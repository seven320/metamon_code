import pytest
import datetime as dt
import json

import random
from src import hometask

@pytest.fixture(scope = "function")
def task_historys():
    data = json.loads('{"count":4,"next":null,"previous":null,"results":[{"tweet_id":19999,"tweet_text":"起きれた","praised":false,"task_id":1,"created_at":"2020-08-24T16:50:57.512674","user_id":1234567}, \
        {"tweet_id":19999,"tweet_text":"起きれた","praised":false,"task_id":1,"created_at":"2020-08-26T16:50:57.536801","user_id":1234567}, \
        {"tweet_id":19999,"tweet_text":"起きれた","praised":false,"task_id":1,"created_at":"2020-08-28T21:09:00.654177","user_id":1234567}, \
        {"tweet_id":19999,"tweet_text":"起きれた","praised":false,"task_id":1,"created_at":"2020-08-28T21:09:00.683196","user_id":1234567}]}')
    task_historys = data["results"]
    return task_historys

@pytest.fixture(scope = "function")
def task_historys_3days():
    data = json.loads('{"count":4,"next":null,"previous":null,"results":[{"tweet_id":19999,"tweet_text":"起きれた","praised":false,"task_id":1,"created_at":"2020-08-24T16:50:57.512674","user_id":1234567}, \
        {"tweet_id":19999,"tweet_text":"起きれた","praised":false,"task_id":1,"created_at":"2020-08-26T16:50:57.536801","user_id":1234567}, \
        {"tweet_id":19999,"tweet_text":"起きれた","praised":false,"task_id":1,"created_at":"2020-08-27T21:09:00.654177","user_id":1234567}, \
        {"tweet_id":19999,"tweet_text":"起きれた","praised":false,"task_id":1,"created_at":"2020-08-28T21:09:00.683196","user_id":1234567}]}')
    task_historys = data["results"]
    return task_historys

def test_count_hometask_streak1(task_historys):
    streak_count = hometask.count_hometask_streak(task_historys)
    assert streak_count == 1

def test_count_hometask_streak2(task_historys_3days):
    streak_count = hometask.count_hometask_streak(task_historys_3days)
    assert streak_count == 3