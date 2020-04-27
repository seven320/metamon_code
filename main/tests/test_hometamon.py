import os
import sys

import pytest
import datetime as dt
sys.path.insert(0, os.path.dirname(__file__))

from src import hometamon2

@pytest.fixture(scope = "function")
def app(mocker):
    app = hometamon2.Hometamon()
    app.manuscript = mocker.Mock()
    app.manuscript.reply = ["お疲れ様だもん"]
    app.manuscript.greeting_morning = ["おはようだもん"]
    app.manuscript.greeting_night = ["おやすみだもん"]
    app.manuscript.sweet_tweet_before = ["3時"]
    app.manuscript.sweet_tweet_after = ["休憩するもん"]
    app.manuscript.sweets = ["U+1F950"] # croissant
    app.api = mocker.MagicMock()
    return app

@pytest.fixture(scope = "function")
def tweet(mocker):
    tweet = mocker.MagicMock()
    tweet.text = "おはよう"
    tweet.user.name = "電電"
    tweet.user.screen_name = "yosyuaomenww"
    tweet.favorited = False
    tweet.id = 123
    return tweet

def test_greeting_morning(app, tweet):
    expected = "@yosyuaomenww\n電電おはようだもん"
    assert app.greeting_morning(tweet) == expected
    app.api.update_status.assert_called_once_with(
        status = expected,
        in_reply_to_status_id = 123
        )
    app.api.create_favorite.assert_called_once_with(
        tweet.id
    )

def test_greeting_night(app, tweet):
    expected = "@yosyuaomenww\n電電おやすみだもん"
    assert app.greeting_night(tweet) == expected
    app.api.update_status.assert_called_once_with(
        status = expected,
        in_reply_to_status_id = tweet.id
        )
    app.api.create_favorite.assert_called_once_with(
        tweet.id
    )

def test_praise(app, tweet):
    expected = "@yosyuaomenww\n電電お疲れ様だもん"
    assert app.praise(tweet) == expected
    app.api.update_status.assert_called_once_with(
        status = expected,
        in_reply_to_status_id = tweet.id
        )
    app.api.create_favorite.assert_called_once_with(
        tweet.id
    )

def test_tweet_sweet(app):
    expected = "3時\n⊂・ー・つ🥐\n休憩するもん"
    app.tweet_sweet()
    app.api.update_status.assert_called_once_with(
        status = expected
    )

def test_test_tweet(app):
    expected = "起きてるもん！\n⊂・ー・つ"
    assert app.test_tweet() == expected
    app.api.update_statussert_called_once_with(
        status = expected
    )

def test_check_exclude_text(app, tweet, mocker):
    assert app.check_exclude(tweet) == False
    assert app.check_exclude(mocker.patch.object(tweet, "method", favorited = True)) == True # tweetの属性をpatchで変化させた．
    assert app.check_exclude(mocker.patch.object(tweet, "method", text = "RT おはよう", favorited = False)) == True 
    assert app.check_exclude(mocker.patch.object(tweet, "method", text = "@yosyuaomew おはよう", favorited = False)) == True
    assert app.check_exclude(mocker.patch.object(tweet, "method", text = "*" * 80, favorited = False)) == True 
    assert app.check_exclude(mocker.patch.object(tweet, "method", text = "https://www.google.com/", favorited = False)) == True 
    assert app.check_exclude(mocker.patch.object(tweet, "method", text = "@denden_by ありがとう", favorited = False, id = 123))
    app.api.create_favorite.assert_called_once_with(
        id = 123
    )

def test_check_exclude_user(app, tweet):
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

def test_check_sweet(app):
    app.JST = dt.datetime(2020, 11, 11, 14, 59)
    assert app.check_sweet() == False

    app.JST = dt.datetime(2020, 11, 11, 15, 0)
    assert app.check_sweet() == True

    app.JST = dt.datetime(2020, 12, 25, 20, 8)
    assert app.check_sweet() == False

def test_check_reply(app, tweet, mocker):
    assert app.check_reply(mocker.patch.object(tweet, "method", text = "疲れた")) == True
    assert app.check_reply(mocker.patch.object(tweet, "method", text = "元気いっぱい")) == False

def test_check_transform(app, tweet, mocker):
    tweet.text = "変身"
    assert app.check_transform(mocker.patch.object(tweet, "method", text = "変身")) == True
    assert app.check_transform(mocker.patch.object(tweet, "method", text = "返信")) == False

def test_check_text(app, tweet):
    tweet.text = "__test__"
    tweet.user.screen_name = "yosyuaomenww"
    assert app.check_test(tweet) == True

def test_check_text_1(app, tweet):
    tweet.text = "__test__"
    tweet.user.screen_name = "hogehoge"
    assert app.check_test(tweet) == False

def test_classify_0(app, tweet):
    tweet.text = "http"
    expected = ""
    assert app.classify(tweet) == expected
    app.api.update_statussert_called_once_with(
        status = expected,
        in_reply_to_status_id = tweet.id
        )
    app.api.create_favorite.assert_not_called()

def test_classify_1(app, tweet):
    tweet.text = "おはよう"
    tweet.user.name = "青い鳥"
    expected = "@yosyuaomenww\n青い鳥おはようだもん"
    app.JST = dt.datetime(2020, 2, 21, 8, 0)
    assert app.classify(tweet) == expected
    app.api.update_status.assert_called_once_with(
        status = expected,
        in_reply_to_status_id = tweet.id
        )
    app.api.create_favorite.assert_called_once_with(
        tweet.id
    )

def test_classify_2(app, tweet):
    tweet.text = "寝る"
    expected = "@yosyuaomenww\n電電おやすみだもん"
    app.JST = dt.datetime(2020, 2, 21, 22, 0)
    assert app.classify(tweet) == expected
    app.api.update_status.assert_called_once_with(
        status = expected,
        in_reply_to_status_id = tweet.id
        )
    app.api.create_favorite.assert_called_once_with(
        tweet.id
    )

def text_classify_3(app, tweet):
    tweet.text = "疲れた"
    expected = "@yosyuaomenww\n電電お疲れ様だもん"
    assert app.classify(tweet) == expected
    app.api.update_status.assert_called_once_with(
        status = expected,
        in_reply_to_status_id = tweet.id
    )
    app.api.create_favorite.assert_called_once_with(
        tweet.id
    )

def test_classify_4(app, tweet):
    tweet.text = "今日のメニューはカレーだ"
    expected = ""
    assert app.classify(tweet) == expected
    app.api.update_status.assert_not_called()
    app.api.create_favorite.assert_not_called()

def test_classify_5(app, tweet):
    tweet.text = "__test__"
    expected = "起きてるもん！\n⊂・ー・つ"
    assert app.classify(tweet) == expected
    app.api.update_status.assert_called_once_with(
        status = expected
    )
    expected = ""
    tweet.user.screen_name = "twitter"
    assert app.classify(tweet) == expected

def test_transform(app):
    expected = ""
    assert app.transform() == expected
    assert app.counts["transform"] == 1

def test_followback(app, mocker):
    app.api.followers_ids.return_value = [1220747547607650304, 1125305225198297089]
    app.api.friends_ids.return_value = [1220747547607650304]
    user_status = mocker.Mock()
    user_status.follow_request_sent = False
    user_status.id = 1125305225198297089
    app.api.lookup_users.return_value = [
        user_status
    ]
    app.followback()
    app.api.create_friendship.assert_called_once_with(
        id = 1125305225198297089
    )

    app.api.reset_mock() # 呼び出し回数をリセット
    user_status.follow_request_sent = True
    app.api.lookup_users.return_value = [
        user_status
    ]
    app.followback()
    app.api.create_friendship.assert_not_called()

def test_report(app):
    app.JST = dt.datetime(2020, 4, 27, 17, 40 , 30)
    app.report()
    app.api.send_direct_message.assert_called_once_with(
        '4745437604',
        'time:2020/04/27 17:40:30\n褒めた数:0\n無効な数:0\n挨拶した数:0\n反応しなかった数:0\n変身:0\nテスト数:0\n合計:0だもん！'
    )

