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

    class Test_スクリーンネームからat以降の文字を削除する:
        def test_user_screen_name_changer_small(self, app):
            assert app.user_name_changer("電電@テスト頑張る") == "電電"
        
        def test_user_screen_name_changer_big(self, app):
            assert app.user_name_changer("電電＠テスト頑張る") == "電電"

        def test_user_screen_name_changer(self, app):
            assert app.user_name_changer("電電") == "電電"

    class Test_朝の挨拶を行う:
        def test_greeting_morning(self, app, tweet):
            expected = "@yosyuaomenww\n電電おはようだもん"
            assert app.greeting_morning(tweet) == (expected, False)
            app.api.update_status.assert_called_once_with(
                status = expected,
                in_reply_to_status_id = 123
            )
            app.api.create_favorite.assert_called_once_with(tweet.id)
        
        def test_greeting_morning_with_image(self):
            pass
    
    class Test_夜の挨拶を行う:
        def test_greeting_night(self, app, tweet):
            expected = "@yosyuaomenww\n電電おやすみだもん"
            assert app.greeting_night(tweet, image_ratio = 0) == (expected, False)
            app.api.update_status.assert_called_once_with(
                status = expected,
                in_reply_to_status_id = 123
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

    class Test_褒める:
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

        def test_praise_with_image(self, app, tweet):
            expected = "@yosyuaomenww\n電電お疲れ様だもん"
            assert app.praise(tweet, image_ratio = 1) == (expected, True)
            app.api.update_with_media.assert_called_once_with(
                filename = "images/icon.jpg",
                status = expected,
                in_reply_to_status_id = tweet.id
            )
            app.api.create_favorite.assert_called_once_with(
                tweet.id
            )

    class Test_休憩を促すツイートを行う:
        def test_tweet_sweet(self, app):
            expected = "3時\n⊂・ー・つ🥐\n休憩するもん"
            app.tweet_sweet()
            app.api.update_status.assert_called_once_with(
                status = expected
            )

    class Test_電電のテストツイートに対して反応する:
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

    class Test_定められたツイートに対しては反応しない:
        def test_check_exclude_text(self, app, tweet):
            assert app.check_exclude(tweet) == False

        def test_check_exclude_text_with_favorited(self, app, tweet, mocker):
            assert app.check_exclude(mocker.patch.object(tweet, "method", favorited=True)) == True

        def test_check_exclude_text_with_RT(self, app, tweet, mocker):
            assert app.check_exclude(mocker.patch.object(tweet, "method", text = "RT おはよう", favorited = False)) == True 

        def test_check_exclude_text_with_at(self, app, tweet, mocker):
            assert app.check_exclude(mocker.patch.object(tweet, "method", text = "@yosyuaomew おはよう", favorited = False)) == True

        def test_check_exclude_text_with_long_tweet(self, app, tweet, mocker):
            assert app.check_exclude(mocker.patch.object(tweet, "method", text = "*" * 80, favorited = False)) == True 

        def test_check_exclude_text_with_url(self, app, tweet, mocker):
            assert app.check_exclude(mocker.patch.object(tweet, "method", text = "https://www.google.com/", favorited = False)) == True 

        def test_check_exclude_text_with_at_me(self, app, tweet, mocker):
            assert app.check_exclude(mocker.patch.object(tweet, "method", text = "@denden_by ありがとう", favorited = False, id = 123)) == True

        def test_check_exclude_text_with_mytweet(self, app, tweet, mocker): 
            mocker.patch.object(tweet.user, "id", 966247026416472064)
            assert app.check_exclude(tweet) == True

        def test_check_exclude_with_exclude_user(self, app, tweet):
            tweet.user.name = "botほげ"
            assert app.check_exclude(tweet) == True

    class 日本時間の5_10時の時Trueを返す:
        def test_check_greeting_morning_with_night(self, app, tweet):
            app.JST = dt.datetime(2020, 11, 11, 4, 59)
            assert app.check_greeting_morning(tweet) == False

        def test_check_greeting_night_with_early_morning(self, app, tweet):
            app.JST = dt.datetime(2020, 11, 11, 5, 0)
            assert app.check_greeting_morning(tweet) == True

        def test_check_greeting_morning_with_noon(self, app, tweet):
            app.JST = dt.datetime(2020, 11, 11, 10, 1)
            assert app.check_greeting_morning(tweet) == False

    class 日本時間の22_2時の時Trueを返す:
        def test_check_greeting_night(self, app, tweet):
            app.JST = dt.datetime(2020, 11, 11, 22, 00)
            assert app.check_greeting_night(tweet) == True

        def test_check_greeting_night_with_last(self, app, tweet):
            app.JST = dt.datetime(2020, 11, 11, 1, 59)
            assert app.check_greeting_night(tweet) == True

        def test_check_greeting_night_with_morning(self, app, tweet):
            app.JST = dt.datetime(2020, 11, 11, 5, 00)
            assert app.check_greeting_night(tweet) == False

    class 日本時間の15時にTrueを返す:
        def test_check_sweet_before(self, app):
            app.JST = dt.datetime(2020, 11, 11, 14, 59)
            assert app.check_sweet() == False

        def test_check_sweet_with_15(self, app):
            app.JST = dt.datetime(2020, 11, 11, 15, 0)
            assert app.check_sweet() == True

        def test_check_sweet_with_after(self, app):
            app.JST = dt.datetime(2020, 12, 25, 20, 8)
            assert app.check_sweet() == False

    class Test_返事をするかどうか:
        def test_check_reply(self, app, tweet, mocker):
            assert app.check_reply(mocker.patch.object(tweet, "method", text = "疲れた")) == True

        def test_check_reply_with_false(self, app, tweet, mocker):
            assert app.check_reply(mocker.patch.object(tweet, "method", text = "元気いっぱい")) == False

    class Test_予備機能_変身:
        def test_check_transform(self, app, tweet, mocker):
            assert app.check_transform(mocker.patch.object(tweet, "method", text = "変身")) == True

        def test_check_transform_with_false(self, app, tweet, mocker):
            assert app.check_transform(mocker.patch.object(tweet, "method", text = "返信")) == False

    class Test_test_tweetに対してツイートするかどうか:
        class Test_起動ツイート:
            def test_check_text(self, app, tweet):
                tweet.text = "__test__"
                tweet.user.screen_name = "yosyuaomenww"
                assert app.check_test(tweet) == True

            def test_check_text_with_false(self, app, tweet):
                tweet.text = "__test__"
                tweet.user.screen_name = "hogehoge"
                assert app.check_test(tweet) == False

        class Test_imageを含んだ起動ツイート:
            def test_check_image_flg(self, app, tweet):
                tweet.text = "__test__ image"
                assert app.check_image_flg(tweet) == True

    #################
    ### Join test ### 
    #################

    class Test_ツイート内容に基づいた分類とその反応ができている:
        def test_classify_with_false(self, app, tweet):
            tweet.text = "http"
            expected = ""
            assert app.classify(tweet) == (expected, False)
            app.api.update_statussert_called_once_with(
                status = expected,
                in_reply_to_status_id = tweet.id
                )
            app.api.create_favorite.assert_not_called()

        class Test_おはよう:
            def test_classify_good_morning(self, app, tweet):
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
        
        class Test_おやすみ:
            def test_classify_goodnight(self, app, tweet):
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

            def test_classify_goodnight_with_image(self, app, tweet):
                tweet.text = "寝る"
                expected = "@yosyuaomenww\n電電おやすみだもん"
                app.JST = dt.datetime(2020, 2, 21, 22, 0)
                assert app.classify(tweet, image_ratio=1) == (expected, True)
                app.api.update_with_media.assert_called_once_with(
                    filename="images/oyasumi_w_newtext.jpg",
                    status = expected,
                    in_reply_to_status_id = tweet.id
                    )
                app.api.create_favorite.assert_called_once_with(
                    tweet.id
                )


    

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
