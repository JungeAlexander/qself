import os
from datetime import date
from datetime import datetime
from datetime import timedelta

from dotenv import find_dotenv
from dotenv import load_dotenv

from qself.oura import OuraAPIClient


def test_oura_api_client():
    load_dotenv(find_dotenv())
    client = OuraAPIClient(os.environ["OURA_PERSONAL_ACCESS_TOKEN"])
    da = client("daily_activity", "2022-01-01", "2022-01-02")
    assert da.data[0].day == date(2022, 1, 1)
