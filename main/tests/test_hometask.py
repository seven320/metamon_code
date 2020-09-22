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
def app(mocker, manuscript):
    app = hometask.HomeTask()
    app.manuscript = manuscript
    app.api = mocker.MagicMock()
    return app

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

@pytest.fixture(scope = "function")
def tweet(mocker):
    tweet = mocker.MagicMock()
    tweet.text = "おはよう"
    tweet.user.name = "電電"
    tweet.user.screen_name = "yosyuaomenww"
    tweet.user.id = 555555
    tweet.favorited = False
    tweet.id = 123
    return tweet

def test_count_hometask_streak_1(app, task_historys):
    streak_count = app.count_hometask_streak(task_historys)
    assert streak_count == 1

def test_count_hometask_streak_2(app, task_historys_3days):
    streak_count = app.count_hometask_streak(task_historys_3days)
    assert streak_count == 3

def test_count_hometask_streak_3(app):
    fake_task_historys = [
        {"tweet_id":12,"tweet_text":"#hometask","praised":"false","task_id":2,"created_at":"2020-08-24T02:58:56.298619","user_id":4745437604}
    ]
    assert 1 == app.count_hometask_streak(task_historys = fake_task_historys)


def test_count_hometask_streak_4(app):
    # 不連続
    fake_task_historys = [
        {"tweet_id":12,"tweet_text":"#hometask","praised":"false","task_id":2,"created_at":"2020-08-24T02:58:56.298619","user_id":4745437604},
        {"tweet_id":1299,"tweet_text":"#hometask","praised":"false","task_id":2,"created_at":"2020-08-25T03:09:18.066556","user_id":4745437604},
        {"tweet_id":129940,"tweet_text":"#hometask","praised":"false","task_id":2,"created_at":"2020-08-25T03:09:29.865963","user_id":4745437604}
    ]
    assert 2 == app.count_hometask_streak(task_historys = fake_task_historys)

def test_count_hometask_streak_5(app):
    fake_task_historys = [
        {"tweet_id":12,"tweet_text":"#hometask","praised":"false","task_id":2,"created_at":"2020-08-24T02:58:56.298619","user_id":4745437604},
        {"tweet_id":1299,"tweet_text":"#hometask","praised":"false","task_id":2,"created_at":"2020-08-25T03:09:18.066556","user_id":4745437604},
        {"tweet_id":129940,"tweet_text":"#hometask","praised":"false","task_id":2,"created_at":"2020-08-25T03:09:29.865963","user_id":4745437604},
        {"tweet_id":12994,"tweet_text":"#hometask","praised":"false","task_id":2,"created_at":"2020-08-26T03:09:45.205176","user_id":4745437604},
        {"tweet_id":133,"tweet_text":"#hometask","praised":"false","task_id":2,"created_at":"2020-08-27T03:09:53.256988","user_id":4745437604}
    ]
    streak_count = app.count_hometask_streak(task_historys = fake_task_historys)
    expected_streak_count = 4
    assert expected_streak_count == streak_count

def test_make_icon(app, manuscript):
    fake_count = 1
    icon = app.make_icon(fake_count)
    assert icon == chr(int(manuscript.icon[1],16))
    fake_count = 2
    icon = app.make_icon(fake_count)
    assert icon == chr(int(manuscript.icon[1],16))
    fake_count = 4
    icon = app.make_icon(fake_count)
    assert icon == chr(int(manuscript.icon[1],16))
    fake_count = 5
    icon = app.make_icon(fake_count)
    assert icon == chr(int(manuscript.icon[5],16))
    fake_count = 6
    icon = app.make_icon(fake_count)
    assert icon == chr(int(manuscript.icon[5],16))
    fake_count = 10
    icon = app.make_icon(fake_count)
    assert icon == chr(int(manuscript.icon[10],16))
    fake_count = 30
    icon = app.make_icon(fake_count)
    assert icon == chr(int(manuscript.icon[30],16))
    fake_count = 50
    icon = app.make_icon(fake_count)
    assert icon == chr(int(manuscript.icon[30],16))

def test_praised_random(app, manuscript):
    reply = app.praised_random()
    assert reply == manuscript.hometask_random_reply[0]

def test_praised_count_hometask(app, manuscript):
    for fake_count in [1,5,10,30]:
        expected_reply = manuscript.count_reply[fake_count] + chr(int(manuscript.icon[fake_count], 16))
        reply = app.praised_count_hometask(count = fake_count)
        assert expected_reply == reply

def test_praised_streak(app, manuscript):
    for fake_streak_count in [3, 7, 14]:
        reply = app.praised_streak(streak_count = fake_streak_count)
        expected_reply = manuscript.streak_reply[fake_streak_count]
        assert expected_reply == reply

def test_extract_task(app):
    expected = "本を読む"
    tweet_text = "@denden_by 設定本を読む"
    assert app.extract_task(tweet_text) == expected
    tweet_text = "@denden_by\n設定：本を読む"
    assert app.extract_task(tweet_text) == expected
    tweet_text = "@denden_by\n設定:本を読む"
    assert app.extract_task(tweet_text) == expected
    tweet_text = "@denden_by\n\n 設定本を読む"
    assert app.extract_task(tweet_text) == expected

def test_hometask_exclude(app, tweet, mocker):
    tweet_text = "@denden_by 設定:早起き"
    assert app.hometask_exclude(mocker.patch.object(tweet,"method", text = tweet_text, favorited = False)) == False
    tweet_text = "@denden_by #hometask 起きれた"
    assert app.hometask_exclude(mocker.patch.object(tweet,"method", text = tweet_text, favorited = False))  == False
    tweet_text = "@denden_by #hometask https://www.google.com/?hl=ja"
    assert app.hometask_exclude(mocker.patch.object(tweet,"method", text = tweet_text, favorited = False))  == False
    tweet_text = "@denden_by #hometask https://www.google.com/?hl=ja"
    assert app.hometask_exclude(mocker.patch.object(tweet,"method", text = tweet_text, favorited = True))  == True
    tweet_text = "@yosyuaomenww その設定は草"
    assert app.hometask_exclude(mocker.patch.object(tweet,"method", text = tweet_text, favorited = False))  == True
    tweet_text = "@denden_by ありがとうねえ"
    assert app.hometask_exclude(mocker.patch.object(tweet,"method", text = tweet_text, favorited = False, id = 123))  == True
    app.api.create_favorite.assert_called_once_with(id = tweet.id)




    
