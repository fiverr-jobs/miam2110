
import json
import requests
from lead import Lead
from datetime import datetime, timedelta

class Assfinet():
    def __init__(self):
        self.identifier = ""
        self.secret = ""
        self.url = "https://api.klicktipp.com/list.json"

    def format_lead(self, lead):
        # TODO format Lead in the post request form from Assfinet
        pass
    def post_lead(self, lead):
        
        payload= self.format_lead(lead)
        headers = {
            # TODO set the correct headers
            "content-type": "application/json",
            "cache-control": "no-cache"}
        response = requests.post(self.url, data=payload, headers=headers)
        # TODO check if the lead is correctly saved and sent 200/201 back
        return response