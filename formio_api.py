import json
import aiohttp
from config import formio
from datetime import datetime


class APIException(Exception):
    pass


class FormioWrapper:
    def __init__(self):
        self.email = formio["email"]
        self.password = formio["password"]
        self.base_url = formio["base_url"]

    async def login(self):
        api_url = self.base_url + "/user/login"
        headers = {"Content-Type": "application/json", "User-Agent": "TCS Discord Bot"}
        payload = {"data": {"email": self.email, "password": self.password}}
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, json=payload, headers=headers) as response:
                json_resp = await response.json()
                token = response.headers.get("x-jwt-token")
        return token

    async def get_application_list(self, token):
        api_url = self.base_url + "/tcsapplication/submission?limit=20&sort=-created"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "TCS Discord Bot",
            "x-jwt-token": token,
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, headers=headers) as response:
                json_resp = await response.json()
        return [x["_id"] for x in json_resp]

    async def get_application_info(self, token, app_id):
        api_url = self.base_url + f"/tcsapplication/submission/{app_id}"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "TCS Discord Bot",
            "x-jwt-token": token,
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, headers=headers) as response:
                json_resp = await response.json()
        user_data = {
            "application_id": json_resp["_id"],
            "created": datetime.strptime(json_resp["created"], "%Y-%m-%dT%H:%M:%S.%fZ"),
            "user_id": json_resp["owner"],
            "user_ip": json_resp["metadata"]["headers"]["x-real-ip"],
            "username": json_resp["data"]["username"],
            "age": json_resp["data"]["age"],
            "time_zone": json_resp["metadata"]["timezone"],
            "availability": json_resp["data"]["availability"],
            "steam_account": json_resp["data"]["steamProfile"],
            "referral": json_resp["data"]["referral"],
            "reason": json_resp["data"]["openResponse"],
            "member_referral": None,
            "other_referral": None,
            "email": json_resp["data"]["email"],
        }
        try:
            user_data["member_name"] = json_resp["data"]["memberName"]
        except KeyError:
            pass
        try:
            user_data["other_referral"] = json_resp["data"]["otherReferral"]
        except KeyError:
            pass
        return user_data

    async def logout(self):
        api_url = self.base_url + "/logout"
        headers = {
            "User-Agent": "TCS Discord Bot",
            "x-jwt-token": "",
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, headers=headers) as response:
                assert response.status == 200
