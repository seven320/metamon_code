import pytest

import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from src import hometamon2

from mock import Mock
import datetime as dt

class FakeManuscript():
    def __init__(self):
        self.reply = ["reply"]
        self.greeting_morning = ["おはよう"]
        self.greeting_night = ["こんばんは"]

        self.sweet_tweet_before = ["3時"]
        self.sweet_tweet_after = ["おやすみ"]
        self.sweets = ["U+1F950"] # croissant

@pytest.fixture(scope = "function")
def app():
    app = hometamon2.Hometamon()
    app.manuscript = FakeManuscript()
    return app

@pytest.fixture(scope = "function")
def tweet():
    tweet = Mock()
    tweet.text = "おはよう"
    tweet.user.name = "電電"
    tweet.user.screen_name = "yosyuaomenw"
    tweet.favorited = False
    return tweet

def test_greeting_morning(app):
    expected = "@twitter\n青い鳥おはよう"
    reply = app.greeting_morning(user_name = "青い鳥", screen_name = "twitter")
    assert reply == expected

def test_greeting_night(app):
    expected = "@twitter\n青い鳥こんばんは"
    reply = app.greeting_night(user_name = "青い鳥", screen_name = "twitter")
    assert reply == expected

def test_check_exclude_0(app, tweet): # 除外テスト
    assert app.check_exclude(tweet) == False

def test_check_exclude_1(app, tweet):
    tweet.favorited = True
    assert app.check_exclude(tweet) == True

def test_check_exclude_2(app, tweet):
    tweet.text = "RT おはよう"
    assert app.check_exclude(tweet) == True

def test_check_exclude_3(app, tweet):
    tweet.text = "@yosyuaomenw おはよう"
    assert app.check_exclude(tweet) == True

def test_check_exclude_4(app, tweet):
    tweet.text = "*" * 80
    assert app.check_exclude(tweet) == True

def test_check_exclude_5(app, tweet):
    tweet.text = "https://www.google.com/"
    assert app.check_exclude(tweet) == True
    
def test_check_exclude_6(app, tweet):
    tweet.user.name = "botほげ"
    assert app.check_exclude(tweet) == True

def test_check_greeting_morning(app, tweet):
    app.JST = dt.datetime(2020, 11, 11, 4, 59)
    assert app.check_greeting_morning(tweet) == False

    app.JST = dt.datetime(2020, 11, 11, 5, 0)
    assert app.check_greeting_morning(tweet) == True

    tweet.text = "こんにちは"
    app.JST = dt.datetime(2020, 11, 11, 6, 0)
    assert app.check_greeting_morning(tweet) == False

def test_check_greeting_night(app, tweet):
    tweet.text = "寝る"
    app.JST = dt.datetime(2020, 11, 11, 4, 59)
    assert app.check_greeting_night(tweet) == False

    app.JST = dt.datetime(2020, 11, 11, 22, 00)
    assert app.check_greeting_night(tweet) == True

    app.JST = dt.datetime(2020, 11, 11, 1, 59)
    assert app.check_greeting_night(tweet) == True

def test_check_reply_0(app, tweet):
    tweet.text = "疲れた"
    assert app.check_reply(tweet) == True

def test_check_reply_1(app, tweet):
    tweet = Mock()
    tweet.text = "元気いっぱい"
    assert app.check_reply(tweet) == False

def test_check_transform_0(app, tweet):
    tweet.text = "変身"
    assert app.check_transform(tweet) == True

def test_check_transform_1(app, tweet):
    tweet.text = "返信"
    assert app.check_transform(tweet) == False

def test_check_text(app, tweet):
    tweet.text = "__test__"
    tweet.user.screen_name = "yosyuaomenw"
    assert app.check_test(tweet) == True

def test_check_text_1(app, tweet):
    tweet.text = "__test__"
    tweet.user.screen_name = "hogehoge"
    assert app.check_test(tweet) == False

    


# def test_classify():
#     app = hometamon2.Hometamon()
#     app.manuscript = FakeManuscript()
    
#     tweet = Mock()
#     tweet.text = "寝る"
#     tweet.user.name = "ほげ"
#     tweet.favorited = False 
#     app.JST = dt.datetime(2020, 11, 11, 1, 59)
#     assert app.classify(tweet) == "greeting_night"


