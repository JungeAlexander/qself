from qself.oura_models import OuraWorkoutResponse


def test_oura_workout_response():
    example_workout_response = {
        "data": [
            {
                "activity": "walking",
                "calories": 100,
                "day": "2021-02-01",
                "distance": 1500.5,
                "end_datetime": "2021-02-01T01:00:00.000000+00:00",
                "intensity": "moderate",
                "label": None,
                "source": "manual",
                "start_datetime": "2021-02-01T01:30:00.000000+00:00",
            }
        ],
        "next_token": None,
    }

    owr = OuraWorkoutResponse.parse_obj(example_workout_response)
    assert owr.data[0].activity == "walking"
