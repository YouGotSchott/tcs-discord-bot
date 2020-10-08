import gspread_asyncio
from oauth2client.service_account import ServiceAccountCredentials
from config import helper_sheet


class GoogleHelperSheet:
    def __init__(self):
        pass

    def get_creds(self):
        return ServiceAccountCredentials.from_json_keyfile_name(
            "client_secret.json",
            [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive",
                "https://www.googleapis.com/auth/spreadsheets",
            ],
        )

    async def update_helper_sheet(self, data):
        agcm = gspread_asyncio.AsyncioGspreadClientManager(self.get_creds)
        agc = await agcm.authorize()
        ss = await agc.open_by_key(helper_sheet)
        ws = await ss.worksheet('Sheet1')
        await ws.append_row(data)

