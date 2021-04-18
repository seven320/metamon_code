import os
import sys
import random

import pytest
import datetime as dt

from src import hometamon

class Test_Hometamon():
    @pytest.fixture()
    def app(self, mocker):
        app = hometamon.Hometamon()
        app.manuscript = mocker.Mock()
        app.manuscript.reply = ["お疲れ様だもん"]
        app.manuscript.greeting_morning = ["おはようだもん"]
        app.manuscript.greeting_night = ["おやすみだもん"]
        app.manuscript.sweet_tweet_before = ["3時"]
        app.manuscript.sweet_tweet_after = ["休憩するもん"]
        app.manuscript.sweets = ["1F950"] # croissant
        app.my_twitter_user_id = "966247026416472064"
        app.api = mocker.MagicMock()
        return app

    @pytest.fixture()
    def tweet(self, mocker):
        tweet = mocker.MagicMock()
        tweet.text = "おはよう"
        tweet.user.name = "電電"
        tweet.user.screen_name = "yosyuaomenww"
        tweet.user.id = 555555
        tweet.favorited = False
        tweet.id = 123
        return tweet

    @pytest.fixture()
    def task_tweet(self, mocker):
        task_tweet = mocker.MagicMock()
        task_tweet.text = "@denden_by\nsettask\n本を読む"
        task_tweet.user.name = "ココア"
        task_tweet.user.screen_name = "cocoa"
        task_tweet.favorited = False
        task_tweet.id = 987654
        return task_tweet

    def test_user_screen_name_changer(self, app, tweet):
        tweet.user.name = "電電@テスト頑張る"
        expected = "電電"
        assert app.user_name_changer(tweet) == expected
        tweet.user.name = "nasa＠webアプリ楽しい"
        expected = "nasa"
        assert app.user_name_changer(tweet) == expected
        tweet.user.name = "電電＠テスト頑張る"
        expected = "電電"
        assert app.user_name_changer(tweet) == expected
        
    def test_greeting_morning(self, app, tweet):
        expected = "@yosyuaomenww\n電電おはようだもん"
        assert app.greeting_morning(tweet) == (expected, False)
        app.api.update_status.assert_called_once_with(
            status = expected,
            in_reply_to_status_id = 123
            )
        app.api.create_favorite.assert_called_once_with(
            tweet.id
        )

    def test_greeting_morning_user_name(self, app, tweet):
        expected = "@yosyuaomenww\n電電おはようだもん"
        tweet.user.name = "電電＠TOEIC999点！！！なんてね"
        assert app.greeting_morning(tweet) == (expected, False)
        app.api.update_status.assert_called_once_with(
            status = expected,
            in_reply_to_status_id = 123
            )
        app.api.create_favorite.assert_called_once_with(
            tweet.id
        ) 

    def test_greeting_night(self, app, tweet):
        expected = "@yosyuaomenww\n電電おやすみだもん"
        assert app.greeting_night(tweet, image_ratio=0) == (expected,  False)
        app.api.update_status.assert_called_once_with(
            status = expected,
            in_reply_to_status_id = tweet.id
            )
        app.api.create_favorite.assert_called_once_with(
            tweet.id
        )

    def test_greeting_night_with_image(self, app, tweet):
        expected = "@yosyuaomenww\n電電おやすみだもん"
        assert app.greeting_night(tweet, image_ratio=1) == (expected, True)
        app.api.update_with_media.assert_called_once_with(
            filename="images/oyasumi_w_newtext.jpg",
            status = expected,
            in_reply_to_status_id = tweet.id
            )
        app.api.create_favorite.assert_called_once_with(
            tweet.id
        )

    def test_praise(self, app, tweet):
        expected = "@yosyuaomenww\n電電お疲れ様だもん"
        assert app.praise(tweet, image_ratio = 0) == (expected, False)
        app.api.update_status.assert_called_once_with(
            status = expected,
            in_reply_to_status_id = tweet.id
            )
        app.api.create_favorite.assert_called_once_with(
            tweet.id
        )

    def test_praise_user_name(self, app, tweet):
        expected = "@yosyuaomenww\n電電お疲れ様だもん"
        tweet.user.name = "電電@最近寝不足"
        assert app.praise(tweet, image_ratio = 0) == (expected, False)
        app.api.update_status.assert_called_once_with(
            status = expected,
            in_reply_to_status_id = tweet.id
        )
        app.api.create_favorite.assert_called_once_with(
            tweet.id
        )

    def test_praise_with_image(self, app, tweet):
        expected = "@yosyuaomenww\n電電お疲れ様だもん"
        tweet.user.name = "電電@最近寝不足"
        assert app.praise(tweet, image_ratio = 1) == (expected, True)
        app.api.update_with_media.assert_called_once_with(
            filename = "images/icon.jpg",
            status = expected,
            in_reply_to_status_id = tweet.id
        )
        app.api.create_favorite.assert_called_once_with(
            tweet.id
        )

    def test_tweet_sweet(self, app):
        expected = "3時\n⊂・ー・つ🥐\n休憩するもん"
        app.tweet_sweet()
        app.api.update_status.assert_called_once_with(
            status = expected
        )

    def test_test_tweet(self, app):
        expected = "起きてるもん！\n⊂・ー・つ"
        assert app.test_tweet() == (expected, False)
        app.api.update_status.assert_called_once_with(
            status = expected
        )

    def test_test_tweet_with_image(self, app):
        expected = "起きてるもん！\n⊂・ー・つ"
        assert app.test_tweet(image_flg=True) == (expected, True)
        app.api.update_with_media.assert_called_once_with(
            filename="images/icon.jpg", status = expected
        )

    def test_check_exclude_text(self, app, tweet, mocker):
        assert app.check_exclude(tweet) == False
        assert app.check_exclude(mocker.patch.object(tweet, "method", favorited = True)) == True # tweetの属性をpatchで変化させた．
        assert app.check_exclude(mocker.patch.object(tweet, "method", text = "RT おはよう", favorited = False)) == True 
        assert app.check_exclude(mocker.patch.object(tweet, "method", text = "@yosyuaomew おはよう", favorited = False)) == True
        assert app.check_exclude(mocker.patch.object(tweet, "method", text = "*" * 80, favorited = False)) == True 
        assert app.check_exclude(mocker.patch.object(tweet, "method", text = "https://www.google.com/", favorited = False)) == True 
        assert app.check_exclude(mocker.patch.object(tweet, "method", text = "@denden_by ありがとう", favorited = False, id = 123)) == True
        app.api.create_favorite.assert_called_once_with(
            id = 123
        )

    def test_check_exclude_text_with_mytweet(self, app,tweet, mocker): 
        mocker.patch.object(tweet.user, "id", 966247026416472064)
        assert app.check_exclude(tweet) == True

    def test_check_exclude_text_with_othertweet(self, app, tweet, mocker):
        mocker.patch.object(tweet.user, "id", 12345)
        assert app.check_exclude(tweet) == False

    def test_check_exclude_user(self, app, tweet):
        tweet.user.name = "botほげ"
        assert app.check_exclude(tweet) == True

    def test_check_greeting_morning(self, app, tweet):
        app.JST = dt.datetime(2020, 11, 11, 4, 59)
        assert app.check_greeting_morning(tweet) == False

        app.JST = dt.datetime(2020, 11, 11, 5, 0)
        assert app.check_greeting_morning(tweet) == True

        tweet.text = "こんにちは"
        app.JST = dt.datetime(2020, 11, 11, 6, 0)
        assert app.check_greeting_morning(tweet) == False

    def test_check_greeting_night(self, app, tweet):
        tweet.text = "寝る"
        app.JST = dt.datetime(2020, 11, 11, 4, 59)
        assert app.check_greeting_night(tweet) == False

        app.JST = dt.datetime(2020, 11, 11, 22, 00)
        assert app.check_greeting_night(tweet) == True

        app.JST = dt.datetime(2020, 11, 11, 1, 59)
        assert app.check_greeting_night(tweet) == True

    def test_check_sweet(self, app):
        app.JST = dt.datetime(2020, 11, 11, 14, 59)
        assert app.check_sweet() == False

        app.JST = dt.datetime(2020, 11, 11, 15, 0)
        assert app.check_sweet() == True

        app.JST = dt.datetime(2020, 12, 25, 20, 8)
        assert app.check_sweet() == False

    def test_check_reply(self, app, tweet, mocker):
        assert app.check_reply(mocker.patch.object(tweet, "method", text = "疲れた")) == True
        assert app.check_reply(mocker.patch.object(tweet, "method", text = "元気いっぱい")) == False

    def test_check_transform(self, app, tweet, mocker):
        tweet.text = "変身"
        assert app.check_transform(mocker.patch.object(tweet, "method", text = "変身")) == True
        assert app.check_transform(mocker.patch.object(tweet, "method", text = "返信")) == False

    def test_check_text(self, app, tweet):
        tweet.text = "__test__"
        tweet.user.screen_name = "yosyuaomenww"
        assert app.check_test(tweet) == True

    def test_check_text_1(self, app, tweet):
        tweet.text = "__test__"
        tweet.user.screen_name = "hogehoge"
        assert app.check_test(tweet) == False

    def test_check_image_flg(self, app, tweet):
        tweet.user.screen_name = "yosyuaomenww"
        tweet.text = "__test__"
        assert app.check_image_flg(tweet) == False
        tweet.text = "__test__ image"
        assert app.check_image_flg(tweet) == True

    def test_check_image_flg_1(self, app, tweet):
        tweet.user.screen_name = "dummy"
        tweet.text = "__test__"
        assert app.check_image_flg(tweet) == False

    # def test_check_task(self, app, task_tweet, tweet):
    #     assert app.check_task(task_tweet) == True
    #     assert app.check_task(tweet) == False

    def test_classify_0(self, app, tweet):
        tweet.text = "http"
        expected = ""
        assert app.classify(tweet) == (expected, False)
        app.api.update_statussert_called_once_with(
            status = expected,
            in_reply_to_status_id = tweet.id
            )
        app.api.create_favorite.assert_not_called()

    def test_classify_1(self, app, tweet):
        tweet.text = "おはよう"
        tweet.user.name = "青い鳥"
        expected = "@yosyuaomenww\n青い鳥おはようだもん"
        app.JST = dt.datetime(2020, 2, 21, 8, 0)
        assert app.classify(tweet) == (expected, False)
        app.api.update_status.assert_called_once_with(
            status = expected,
            in_reply_to_status_id = tweet.id
            )
        app.api.create_favorite.assert_called_once_with(
            tweet.id
        )

    def test_classify_2(self, app, tweet):
        tweet.text = "寝る"
        expected = "@yosyuaomenww\n電電おやすみだもん"
        app.JST = dt.datetime(2020, 2, 21, 22, 0)
        assert app.classify(tweet, image_ratio=0) == (expected, False)
        app.api.update_status.assert_called_once_with(
            status = expected,
            in_reply_to_status_id = tweet.id
            )
        app.api.create_favorite.assert_called_once_with(
            tweet.id
        )
        assert app.classify(tweet, image_ratio=1) == (expected, True)

    def text_classify_3(self, app, tweet):
        tweet.text = "疲れた"
        expected = "@yosyuaomenww\n電電お疲れ様だもん"
        assert app.classify(tweet) == (expected, False)
        app.api.update_status.assert_called_once_with(
            status = expected,
            in_reply_to_status_id = tweet.id
        )
        app.api.create_favorite.assert_called_once_with(
            tweet.id
        )

    def test_classify_4(self, app, tweet):
        tweet.text = "今日のメニューはカレーだ"
        expected = ""
        assert app.classify(tweet) == (expected, False)
        app.api.update_status.assert_not_called()
        app.api.create_favorite.assert_not_called()

    def test_classify_5(self, app, tweet):
        tweet.text = "__test__"
        expected = "起きてるもん！\n⊂・ー・つ"
        assert app.classify(tweet) == (expected, False)
        app.api.update_status.assert_called_once_with(
            status = expected
        )
        # app.api.update_with_media.assert_called_once_with(
        #     filename="images/icon.jpg", status = expected
        # )
        expected = ""
        tweet.user.screen_name = "twitter"
        assert app.classify(tweet) == (expected, False)

    def test_classify_6(self, app, tweet):
        tweet.text = "__test__ image"
        expected = "起きてるもん！\n⊂・ー・つ"
        assert app.classify(tweet) == (expected, True)
        app.api.update_with_media.assert_called_once_with(
            status = expected, filename="images/icon.jpg"
        )
        expected = ""
        tweet.user.screen_name = "twitter"
        assert app.classify(tweet) == (expected, False)

    def test_transform(self, app):
        expected = ""
        assert app.transform() == (expected, False)
        assert app.counts["transform"] == 1

    def test_followback(self, app, mocker):
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

    def test_report(self, app):
        app.JST = dt.datetime(2020, 4, 27, 17, 40 , 30)
        app.admin_twitter_id = 999
        app.report()
        app.api.send_direct_message.assert_called_once_with(
            999,
            'time:2020/04/27 17:40:30\n褒めた数:0\n除外した数:0\n挨拶した数:0\n反応しなかった数:0\n変身:0\nテスト数:0\n合計:0だもん！'
        )
