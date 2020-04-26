import pytest

import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from src import hometamon2

from mock import Mock

class FakeManuscript():
    def __init__(self):
        self.reply = ["reply"]
        self.greeting_morning = ["おはよう"]
        self.greeting_night = ["こんばんは"]

        self.sweet_tweet_before = ["3時"]
        self.sweet_tweet_after = ["おやすみ"]
        self.sweets = ["U+1F950"] # croissant

def test_greetin_morning():
    app = hometamon2.Hometamon()
    app.manuscript = FakeManuscript()
    result = "@twitter\n青い鳥おはよう"
    reply = app.greeting_morning(user_name = "青い鳥", screen_name = "twitter")
    assert result == reply

def test_greeting_night():
    app = hometamon2.Hometamon()
    app.manuscript = FakeManuscript()
    result = "@twitter\n青い鳥こんばんは"
    reply = app.greeting_night(user_name = "青い鳥", screen_name = "twitter")
    assert result == reply

def test_check_exclude(): # 除外テスト
    app = hometamon2.Hometamon()
    app.manuscript = FakeManuscript()

    tweet = Mock()
    tweet.text = "おはよう"
    tweet.user.name = "電電"
    tweet.favorited = False
    assert app.check_exclude(tweet) == False

    tweet.text = "おはよう"
    tweet.user.name = "電電"
    tweet.favorited = True
    assert app.check_exclude(tweet) == True

    tweet.text = "RT おはよう"
    tweet.user.name = "電電"
    tweet.favorited = False
    assert app.check_exclude(tweet) == True

    tweet.text = "@yosyuaomenw おはよう"
    tweet.user.name = "電電"
    tweet.favorited = False
    assert app.check_exclude(tweet) == True

    tweet.text = "*" * 80
    tweet.user.name = "電電"
    tweet.favorited = False
    assert app.check_exclude(tweet) == True

    tweet.text = "https://www.google.com/"
    tweet.user.name = "電電"
    tweet.favorited = False
    assert app.check_exclude(tweet) == True
    
    tweet.text = "おはよう"
    tweet.user.name = "botほげ"
    tweet.favorited = False
    assert app.check_exclude(tweet) == True

# @pytest.fixture(scope = "session")
# def test_










