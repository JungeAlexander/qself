# Functionality to interact with the Oura API.

__all__ = ["OuraAPIClient"]

from datetime import date, datetime, timedelta
import logging
import os

from dotenv import load_dotenv
import httpx

from .oura_models import OuraGenericResponse, OuraWorkoutResponse


class OuraAPIClient:
    """
    Client for the Oura API.
    """

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

    ENDPOINT_TO_RESPONSE_MODEL = {
        "activity": OuraGenericResponse,
        "bedtime": OuraGenericResponse,
        "daily_activity": OuraGenericResponse,
        "heartrate": OuraGenericResponse,
        "personal_info": OuraGenericResponse,
        "readiness": OuraGenericResponse,
        "session": OuraGenericResponse,
        "sleep": OuraGenericResponse,
        "tag": OuraGenericResponse,
        "workout": OuraWorkoutResponse,
    }

    API_VERSION_TO_BASE_URL = {
        "v1": "https://api.ouraring.com/v1",
        "v2": "https://api.ouraring.com/v2/usercollection",
    }

    API_VERSION_TO_DATE_POSTFIX = {"v1": "", "v2": "_date"}

    def __init__(self, personal_token: str):
        """Initialize the client.

        :param personal_token: personal access token for the Oura API
        :type personal_token: str
        """
        self.personal_token = personal_token

    def __call__(
        self,
        endpoint: str,
        start: str | None = None,
        end: str | None = None,
        *,
        next_token=None,
        i=0,
    ) -> OuraGenericResponse:
        api_version = self.ENDPOINT_TO_API_VERSION[endpoint]
        if api_version != "v2" and next_token is not None:
            raise ValueError("Only v2 API supports next_token argument.")
        base_url = self.API_VERSION_TO_BASE_URL[api_version]
        start_param = f"start{self.API_VERSION_TO_DATE_POSTFIX[api_version]}"
        end_param = f"end{self.API_VERSION_TO_DATE_POSTFIX[api_version]}"
        url = f"{base_url}/{endpoint}"  # TODO more robust URL joining
        if start is None:
            params = {} if end is None else {end_param: end}
        else:
            params = {
                start_param: start,
                end_param: end,
            }  # TODO what if end is None? test this
        if next_token is not None:
            params["next_token"] = next_token
        headers = {"Authorization": f"Bearer {self.personal_token}"}
        response = httpx.request("GET", url, headers=headers, params=params)
        response.raise_for_status()
        j = response.json()
        model = self.ENDPOINT_TO_RESPONSE_MODEL[endpoint].parse_obj(j)
        if model.next_token is not None:
            logging.debug(
                f"Using continuation token {i}, last_date {model.data[-1].day}: {model.next_token}"
            )
            new_start = (model.data[-1].day + timedelta(days=1)).isoformat()
            j_new = self(endpoint, new_start, end, next_token=model.next_token, i=i + 1)
            model.data.extend(j_new.data)
        return model
