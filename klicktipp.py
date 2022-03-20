from hmac import new
import json
import requests
from lead import Lead
from urllib.parse import urljoin


class Klicktipp:
    def __del__(self):
        self.logout()

    def __init__(self):
        self.username = "bosydadaq-api"
        self.password = "Start123!"
        self.host = "https://api.klicktipp.com"
        self.login_uri = "account/login.json"
        self.logout_uri = "account/logout.json"
        self.subscribe_uri = "subscriber.json"
        self.tag_uri = "subscriber/tag.json"
        self.headers = {
            "content-type": "application/json",
            "cache-control": "no-cache",
        }
        self.session_name = ""
        self.session_id = ""
        self.login()

    def login(self):
        payload = {"username": self.username, "password": self.password}
        response = requests.post(
            urljoin(self.host, self.login_uri), json=payload, headers=self.headers
        )
        if response.ok:
            response = json.loads(response.text)
            self.headers["Cookie"] = response["session_name"] + "=" + response["sessid"]
        else:
            raise Exception("Klicktipp Request Error")

    def logout(self):
        payload = {"username": self.username, "password": self.password}
        response = requests.post(
            urljoin(self.host, self.logout_uri), json=payload, headers=self.headers
        )
        if response.ok:
            return True
        else:
            raise Exception("Klicktipp Request Error")

    def format_data_field(self, data):
        data = data.replace("'", '"')
        data = json.loads(data)
        new_string = ""
        for attr in data:
            new_string += "{} : {}\n".format(attr, data[attr] if data[attr] else "---")
        return new_string

    def format_lead_tags(self, lead):
        finanzen_de_tag = "8466566"
        variable_tag_list = {
            "gebäude,wohn": "8470942",
            "hund": "8472359",
            "katze": "8472360",
            "pferd": "8472361",
            "zusatz": "8472367",
            "gewerbehaftpflicht": "8472376",
            "gewerbe": "8472377",
        }

        tags = []
        tags.append(finanzen_de_tag)
        for tag in variable_tag_list:
            if lead.subject.lower().find(tag) >= 0:
                tags.append(variable_tag_list[tag])
        payload = {"email": lead.email, "tagids": tags}
        return payload

    def format_lead(self, lead):
        # TODO if the number starts with 01 then push it as smsnumber
        payload = {
            "email": lead.email,
            "listid": "254408",  # single opt in Id
            "fields": {
                "fieldFirstName": lead.firstName,
                "fieldLastName": lead.lastName,
                "fieldStreet1": lead.street,
                "fieldCity": lead.city,
                "fieldState": lead.state,
                "fieldZip": lead.postalCode,
                "fieldCompanyName": lead.company,
                "fieldPhone": lead.phone,
                "field157202": lead.salutation,
                "field157376": lead.gender,
                "field157204": lead.occupation,
                "field164400": lead.email,
                "field164401": lead.subject,
                "field164894": "Finanzen.de Id Number {}".format(lead.id),
                "field164895": lead.createdAt,
                "field165010": lead.dateOfBirth,
                "field165011": self.format_data_field(lead.data),
            },
        }
        return payload

    def post_tags(self, lead):
        payload = self.format_lead_tags(lead)
        response = requests.post(
            urljoin(self.host, self.tag_uri), json=payload, headers=self.headers
        )
        if response.ok:
            return response
        else:
            raise Exception("Klicktipp Request Error")

    def post_lead(self, lead):
        payload = self.format_lead(lead)
        response = requests.post(
            urljoin(self.host, self.subscribe_uri), json=payload, headers=self.headers
        )
        if response.ok:
            self.post_tags(lead)
            return response
        else:
            raise Exception("Klicktipp Request Error")
