import json
import aiohttp
from config import enjin
from datetime import datetime
import pytz


class APIException(Exception):
    pass


class EnjinWrapper:
    def __init__(self):
        self.email = enjin["email"]
        self.password = enjin["password"]
        self.api_url = enjin["api_url"]

    async def login(self):
        payload = {
            "jsonrpc": "2.0",
            "id": "0",
            "params": {"email": self.email, "password": self.password},
            "method": "User.login",
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, json=payload) as response:
                json_resp = json.loads(await response.text())
        if "error" in json_resp:
            raise APIException(json_resp["error"]["message"])
        return json_resp["result"]["session_id"]

    async def get_application_list(self, session_id, app_type, page=1):
        payload = {
            "jsonrpc": "2.0",
            "id": "0",
            "params": {"session_id": session_id, "type": app_type, "page": page},
            "method": "Applications.getList",
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, json=payload) as response:
                json_resp = json.loads(await response.text())
        if "error" in json_resp:
            raise APIException(json_resp["error"]["message"])
        return [x["application_id"] for x in json_resp["result"]["items"]]

    async def get_application_info(self, session_id, app):
        payload = {
            "jsonrpc": "2.0",
            "id": "0",
            "params": {"session_id": session_id, "application_id": app},
            "method": "Applications.getApplication",
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, json=payload) as response:
                json_resp = json.loads(await response.text())
        if "error" in json_resp:
            raise APIException(json_resp["error"]["message"])
        if not json_resp["result"]["title"]:
            return None
        user_data = {
            "application_id": int(json_resp["result"]["application_id"]),
            "created": datetime.utcfromtimestamp(
                int(json_resp["result"]["created"])
            ).replace(tzinfo=pytz.utc),
            "user_id": int(json_resp["result"]["user_id"]),
            "user_ip": json_resp["result"]["user_ip"],
            "username": json_resp["result"]["username"],
            "age": json_resp["result"]["user_data"]["ujkk6920k3"],
            "time_zone": json_resp["result"]["user_data"]["nl6kpkzetq"],
            "availability": json_resp["result"]["user_data"]["uk0masnzu4"],
            "steam_account": json_resp["result"]["user_data"]["ar4cgqsnu5"],
            "referral": json_resp["result"]["user_data"]["gsinqip50v"],
            "reason": json_resp["result"]["user_data"]["kqm2bqnnix"],
        }
        return user_data

    async def approve_applications(self, session_id, apps):
        payload = {
            "jsonrpc": "2.0",
            "id": "0",
            "params": {"session_id": session_id, "application_id": apps},
            "method": "Applications.approve",
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, json=payload) as response:
                json_resp = json.loads(await response.text())
        if "error" in json_resp:
            raise APIException(json_resp["error"]["message"])

    async def decline_applications(self, session_id, apps):
        payload = {
            "jsonrpc": "2.0",
            "id": "0",
            "params": {"session_id": session_id, "application_id": apps},
            "method": "Applications.reject",
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, json=payload) as response:
                json_resp = json.loads(await response.text())
        if "error" in json_resp:
            raise APIException(json_resp["error"]["message"])

    async def send_message(self, session_id, data_subject, data_body, user_ids):
        payload = {
            "jsonrpc": "2.0",
            "id": "0",
            "params": {
                "session_id": session_id,
                "message_subject": data_subject,
                "message_body": data_body,
                "recipients": user_ids,
            },
            "method": "Messages.sendMessage",
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, json=payload) as response:
                json_resp = json.loads(await response.text())
        if "error" in json_resp:
            raise APIException(json_resp["error"]["message"])
