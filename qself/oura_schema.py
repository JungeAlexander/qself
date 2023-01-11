# AUTOGENERATED! DO NOT EDIT! File to edit: ../01_oura_schemas.ipynb.

# %% auto 0
__all__ = ['OuraResponse', 'WorkoutIntensityEnum', 'OuraWorkoutData', 'OuraWorkoutResponse']

# %% ../01_oura_schemas.ipynb 2
import datetime
from enum import Enum

from pydantic import BaseModel, Field

# %% ../01_oura_schemas.ipynb 3
class OuraResponse(BaseModel):
    data: list
    next_token: str | None = Field(..., description="Continuation token")

class WorkoutIntensityEnum(str, Enum):
    easy = 'easy'
    moderate = 'moderate'
    hard = 'hard'

class OuraWorkoutData(BaseModel):
    activity: str = Field(..., description="Name of the activity")
    calories: int | None = Field(..., description="Active calorie burn")
    day: datetime.date = Field(..., description="Date of the activity")
    distance: float | None = Field(..., description="Distance covered")
    end_datetime: datetime.datetime = Field(..., description="End date and time")
    intensity: WorkoutIntensityEnum = Field(..., description="Workout intensity")
    label: str | None = Field(..., description="Label of the activity")
    source: str = Field(..., description="Source of the activity")
    start_datetime: datetime.datetime = Field(..., description="Start date and time")

class OuraWorkoutResponse(OuraResponse):
    data: list[OuraWorkoutData]
