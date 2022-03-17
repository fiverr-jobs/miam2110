import json
import unicodedata
from unittest import case
import requests
from lead import Lead
from datetime import datetime, timedelta


class Finanzen:
    def __init__(self):
        self.identifier = "service@miam-makler.de"
        self.secret = "HmkL68GfRe&#69"
        self.url = "https://de.fgrp.net/api/json.php"
        self.content_type = "application/json"
        self.jsonrpc = "2.0"
        self.method = "lead.getList"
        self.id = "1"

    def create_json_request(self, limit, offset, dataFrom):
        if not offset:
            offset = 0
        json_request = {
            "jsonrpc": self.jsonrpc,
            "method": self.method,
            "params": {
                "request": {
                    "credential": {
                        "identifier": self.identifier,
                        "secret": self.secret,
                    },
                    "filter": {
                        "startDate": "0000-00-00",
                        "soldAtMin": dataFrom,
                        "limit": limit,
                        "offset": offset,
                    },
                }
            },
            "id": self.id,
        }
        return json.dumps(json_request)

    def format_lead(self, lead):
        payload = {
            "id": lead["id"],
            "salutation": lead["customer"]["contact"]["sex"],
            "gender": lead["customer"]["contact"]["sex"],
            "firstName": lead["customer"]["contact"]["firstName"],
            "lastName": lead["customer"]["contact"]["lastName"],
            "dateOfBirth": lead["customer"]["dateOfBirth"],
            "occupation": lead["customer"]["occupationGroup"]["name"],
            "phone": lead["customer"]["phone"],
            "email": lead["customer"]["email"],
            "street": lead["customer"]["street"],
            "postalCode": lead["customer"]["postalCode"],
            "city": lead["customer"]["city"],
            "state": lead["customer"]["postalArea"]["region1"],
            "company": lead["customer"]["contact"]["company"],
            "subject": lead["product"]["name"],
            "data": lead["data"],
            "createdAt": lead["createdAt"]["date"],
        }
        if payload["salutation"] == 1:
            payload["salutation"] = "Herr"
            payload["gender"] = "Männlich"
        elif payload["salutation"] == 2:
            payload["salutation"] = "Frau"
            payload["gender"] = "Weiblich"
        elif payload["salutation"] == 0:
            payload["salutation"] = "Divers"
            payload["gender"] = "Divers"
        else:
            payload["salutation"] = "Unbekannt"

        payload["data"] = json.loads(
            json.dumps(payload["data"], ensure_ascii=False).replace("\xa0", " ")
        )

        return payload

    def get_leads(self, limit, offset, dateFrom):

        payload = self.create_json_request(limit, offset, dateFrom)
        headers = {"content-type": "application/json", "cache-control": "no-cache"}
        response = requests.post(self.url, data=payload, headers=headers)
        if response.ok:
            # response.text = response.text.
            formated_response = json.loads(response.text)["result"]["list"]
            return formated_response
        else:
            raise Exception("Finanzen Request Error")

    def initial_pull(self):
        dateFrom = "000-00-00 00:00:00"
        offset = 0
        limit = 10
        done = False
        leads = []
        while not done:
            loop_leads = self.get_leads(limit, offset, dateFrom)
            for lead in loop_leads["items"]:
                leads.append(Lead(self.format_lead(lead)))
            if len(leads) == loop_leads["count"]:
                done = True
            else:
                offset += 10
        return leads

    def last_day_pull(self):
        since_yesterday = datetime.now() - timedelta(days=1)
        dateFrom = str(since_yesterday)
        offset = 0
        limit = 10
        done = False
        leads = []
        while not done:
            loop_leads = self.get_leads(limit, offset, dateFrom)
            for lead in loop_leads["items"]:
                leads.append(Lead(self.format_lead(lead)))
            if len(leads) == loop_leads["count"]:
                done = True
            else:
                offset += 10
        return leads
