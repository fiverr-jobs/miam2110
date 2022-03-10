import json
import requests
import time
import datetime
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
        self.headers = {
            "content-type": "application/x-www-form-urlencoded",
            "cache-control": "no-cache",
        }
        self.session_name = ""
        self.session_id = ""
        self.login()

    def login(self):
        payload = {"username": self.username, "password": self.password}
        response = requests.post(
            urljoin(self.host, self.login_uri), data=payload, headers=self.headers
        )
        if response.ok:
            response = json.loads(response.text)
            self.headers["Cookie"] = response["session_name"] + "=" + response["sessid"]
        else:
            raise Exception("Klicktipp Request Error")

    def logout(self):
        payload = {"username": self.username, "password": self.password}
        response = requests.post(
            urljoin(self.host, self.logout_uri), data=payload, headers=self.headers
        )
        if response.ok:
            return True
        else:
            raise Exception("Klicktipp Request Error")

    def format_data_field(self, data):
        data = data.replace("'", '"')
        new_string = ""
        for attr in data:
            new_string += "{} : {}\n".format(attr, data[attr])
        return new_string

    def format_lead(self, lead):
        # TODO if the number starts with 01 then push it as smsnumber
        formated_lead = {
            "email": lead.email,
            "fields": {
                "fieldFirstName": lead.firstName,
                "fieldLastName": lead.lastName,
                "fieldStreet1": lead.street,
                "fieldCity": lead.city,
                "fieldState": lead.state,
                "fieldZip": lead.postalCode,
                "fieldCompanyName": lead.company,
                "fieldPhone": lead.phone,
                "fieldBirthday": time.mktime(
                    datetime.datetime.strptime(lead.dateOfBirth, "%Y-%m-%d").timetuple()
                ),
                "field157202": lead.salutation,
                "field157204": lead.occupation,
                "field164400": lead.email,
                "field164401": lead.subject,
                "field164402": "Finanzen.de Id Number {}".format(lead.id),
                "field164535": time.mktime(
                    datetime.datetime.strptime(
                        lead.createdAt, "%Y-%m-%d %H:%M:%S.%f"
                    ).timetuple()
                ),
            },
        }
        return formated_lead

    def post_lead(self, lead):
        payload = self.format_lead(lead)
        print(lead.data)
        # print(payload)
        # response = requests.post(self.url, data=payload, headers=self.headers)
        # if response.ok:
        #     return response
        # else:
        #     raise Exception("Klicktipp Request Error")
