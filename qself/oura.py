# AUTOGENERATED! DO NOT EDIT! File to edit: ../00_oura.ipynb.

# %% auto 0
__all__ = ['OuraAPIClient']

# %% ../00_oura.ipynb 2
from datetime import date, datetime, timedelta
import logging
import os

from dotenv import load_dotenv
import requests

# %% ../00_oura.ipynb 3
class OuraAPIClient:

    ENDPOINT_TO_API_VERSION = {
        "activity": "v1",
        "bedtime": "v1",
        "daily_activity": "v2",
        "heartrate": "v2",
        "personal_info": "v2",
        "readiness": "v1",
        "session": "v2",
        "sleep": "v1",
        "tag": "v2",
        "workout": "v2",
    }

    API_VERSION_TO_BASE_URL = {
        "v1": "https://api.ouraring.com/v1",
        "v2": "https://api.ouraring.com/v2/usercollection",
    }

    API_VERSION_TO_DATE_POSTFIX = {"v1": "", "v2": "_date"}

    def __init__(self, personal_token):
        self.personal_token = personal_token

    def __call__(
        self, endpoint: str, start: str = None, end: str = None, *, next_token=None, i=0
    ):
        api_version = self.ENDPOINT_TO_API_VERSION[endpoint]
        if api_version != "v2" and next_token is not None:
            raise ValueError("Only v2 API supports next_token argument.")
        base_url = self.API_VERSION_TO_BASE_URL[api_version]
        start_param = f"start{self.API_VERSION_TO_DATE_POSTFIX[api_version]}"
        end_param = f"end{self.API_VERSION_TO_DATE_POSTFIX[api_version]}"
        url = f"{base_url}/{endpoint}"  # TODO more robust URL joining
        if start is None:
            params = None if end is None else {end_param: end}
        else:
            params = {
                start_param: start,
                end_param: end,
            }  # TODO what if end is None? test this
        if next_token is not None:
            params["next_token"] = next_token
        headers = {"Authorization": f"Bearer {self.personal_token}"}
        response = requests.request("GET", url, headers=headers, params=params)
        j = response.json()  # TODO check status code and handle errors
        if ("next_token" in j) and (j["next_token"] is not None):
            logging.debug(
                f"Using continuation token {i}, last_date {j['data'][-1]['day']}: {j['next_token']}"
            )
            new_start = (
                date.fromisoformat(j["data"][-1]["day"]) + timedelta(days=1)
            ).isoformat()
            j_new = self(endpoint, new_start, end, next_token=j["next_token"], i=i + 1)
            j["data"].extend(j_new["data"])
        return j
