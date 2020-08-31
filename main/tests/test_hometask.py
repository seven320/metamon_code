import pytest
import datetime as dt
import json

import random
from src import hometask
from src import meta_manuscript

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

@pytest.fixture(scope = "function")
def manuscript():
    manuscript = meta_manuscript.Manuscript()
    manuscript.hometask_random_reply = ["#hometaskできてえらいもん!!!"]
    return manuscript

@pytest.fixture(scope = "function")
def api(mocker):
    api = mocker.MagicMock()
    response = mocker.MagicMock()
    response.status_code.return_value = 200
    data = {
        "count":5,
        "results":[
            {"tweet_id":12,"tweet_text":"#hometask","praised":false,"task_id":2,"created_at":"2020-08-24T02:58:56.298619","user_id":4745437604},
            {"tweet_id":1299,"tweet_text":"#hometask","praised":false,"task_id":2,"created_at":"2020-08-25T03:09:18.066556","user_id":4745437604},
            {"tweet_id":129940,"tweet_text":"#hometask","praised":false,"task_id":2,"created_at":"2020-08-25T03:09:29.865963","user_id":4745437604},
            {"tweet_id":12994,"tweet_text":"#hometask","praised":false,"task_id":2,"created_at":"2020-08-26T03:09:45.205176","user_id":4745437604},
            {"tweet_id":133,"tweet_text":"#hometask","praised":false,"task_id":2,"created_at":"2020-08-29T03:09:53.256988","user_id":4745437604}
            ]
    }
    response.data.return_value = data
    api.search_task_history.return_value = response
    return api

def test_count_hometask_streak1(task_historys):
    streak_count = hometask.count_hometask_streak(task_historys)
    assert streak_count == 1

def test_count_hometask_streak2(task_historys_3days):
    streak_count = hometask.count_hometask_streak(task_historys_3days)
    assert streak_count == 3

# def test_classify_reply(manuscript, api):
#     reply, count = hometask.classify_reply(user_id = 4745437604, manuscript = manuscript, api = api)


def test_count_hometask_streak_1():
    fake_task_historys = [
        {"tweet_id":12,"tweet_text":"#hometask","praised":"false","task_id":2,"created_at":"2020-08-24T02:58:56.298619","user_id":4745437604}
    ]
    assert 1 == hometask.count_hometask_streak(task_historys = fake_task_historys)


def test_count_hometask_streak_2():
    # 不連続
    fake_task_historys = [
        {"tweet_id":12,"tweet_text":"#hometask","praised":"false","task_id":2,"created_at":"2020-08-24T02:58:56.298619","user_id":4745437604},
        {"tweet_id":1299,"tweet_text":"#hometask","praised":"false","task_id":2,"created_at":"2020-08-25T03:09:18.066556","user_id":4745437604},
        {"tweet_id":129940,"tweet_text":"#hometask","praised":"false","task_id":2,"created_at":"2020-08-25T03:09:29.865963","user_id":4745437604}
    ]
    assert 2 == hometask.count_hometask_streak(task_historys = fake_task_historys)

def test_count_hometask_streak_4():
    fake_task_historys = [
        {"tweet_id":12,"tweet_text":"#hometask","praised":"false","task_id":2,"created_at":"2020-08-24T02:58:56.298619","user_id":4745437604},
        {"tweet_id":1299,"tweet_text":"#hometask","praised":"false","task_id":2,"created_at":"2020-08-25T03:09:18.066556","user_id":4745437604},
        {"tweet_id":129940,"tweet_text":"#hometask","praised":"false","task_id":2,"created_at":"2020-08-25T03:09:29.865963","user_id":4745437604},
        {"tweet_id":12994,"tweet_text":"#hometask","praised":"false","task_id":2,"created_at":"2020-08-26T03:09:45.205176","user_id":4745437604},
        {"tweet_id":133,"tweet_text":"#hometask","praised":"false","task_id":2,"created_at":"2020-08-27T03:09:53.256988","user_id":4745437604}
    ]
    streak_count = hometask.count_hometask_streak(task_historys = fake_task_historys)
    expected_streak_count = 4
    assert expected_streak_count == streak_count

def test_make_icon(manuscript):
    fake_count = 1
    icon = hometask.make_icon(fake_count, manuscript)
    assert icon == chr(int(manuscript.icon[1],16))
    fake_count = 2
    icon = hometask.make_icon(fake_count, manuscript)
    assert icon == chr(int(manuscript.icon[1],16))
    fake_count = 4
    icon = hometask.make_icon(fake_count, manuscript)
    assert icon == chr(int(manuscript.icon[1],16))
    fake_count = 5
    icon = hometask.make_icon(fake_count, manuscript)
    assert icon == chr(int(manuscript.icon[5],16))
    fake_count = 6
    icon = hometask.make_icon(fake_count, manuscript)
    assert icon == chr(int(manuscript.icon[5],16))
    fake_count = 10
    icon = hometask.make_icon(fake_count, manuscript)
    assert icon == chr(int(manuscript.icon[10],16))
    fake_count = 30
    icon = hometask.make_icon(fake_count, manuscript)
    assert icon == chr(int(manuscript.icon[30],16))
    fake_count = 50
    icon = hometask.make_icon(fake_count, manuscript)
    assert icon == chr(int(manuscript.icon[30],16))

def test_praised_random(manuscript):
    reply = hometask.praised_random(manuscript)
    assert reply == manuscript.hometask_random_reply[0]

def test_praised_count_hometask(manuscript):
    for fake_count in [1,5,10,30]:
        expected_reply = manuscript.count_reply[fake_count] + chr(int(manuscript.icon[fake_count], 16))
        reply = hometask.praised_count_hometask(count = fake_count, manuscript = manuscript)
        assert expected_reply == reply

def test_praised_streak(manuscript):
    for fake_streak_count in [3, 7, 14]:
        reply = hometask.praised_streak(streak_count = fake_streak_count, manuscript = manuscript)
        expected_reply = manuscript.streak_reply[fake_streak_count]
        assert expected_reply == reply


