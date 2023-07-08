__all__ = [
    "OuraBaseResponse",
    "WorkoutIntensityEnum",
    "OuraGenericData",
    "OuraGenericResponse",
    "OuraWorkoutData",
    "OuraWorkoutResponse",
]

import datetime
from enum import Enum

from pydantic import BaseModel, Extra, Field


class OuraBaseResponse(BaseModel):
    """
    Basic Oura API response model
    """

    data: list
    next_token: str | None = Field(..., description="Continuation token")


class WorkoutIntensityEnum(str, Enum):
    """
    Enum for workout intensity
    """

    easy = "easy"
    moderate = "moderate"
    hard = "hard"


class OuraGenericData(BaseModel):
    """
    Generic Oura data point
    """

    day: datetime.date = Field(..., description="Date of the activity")

    class Config:
        extra = Extra.allow


class OuraGenericResponse(OuraBaseResponse):
    """
    Generic Oura API response model including a list of data points
    """

    data: list[OuraGenericData]


class OuraWorkoutData(BaseModel):
    """
    Oura workout data point
    """

    activity: str = Field(..., description="Name of the activity")
    calories: int | None = Field(..., description="Active calorie burn")
    day: datetime.date = Field(..., description="Date of the activity")
    distance: float | None = Field(..., description="Distance covered")
    end_datetime: datetime.datetime = Field(..., description="End date and time")
    intensity: WorkoutIntensityEnum = Field(..., description="Workout intensity")
    label: str | None = Field(..., description="Label of the activity")
    source: str = Field(..., description="Source of the activity")
    start_datetime: datetime.datetime = Field(..., description="Start date and time")


class OuraWorkoutResponse(OuraBaseResponse):
    """
    Oura API response model including a list of workout data points
    """

    data: list[OuraWorkoutData]
