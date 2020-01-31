# encoding utf-8

import datetime
import tweepy
import random

# 親ディレクトリにあるアカウント情報へのパス
import sys, os

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)

from dotenv import load_dotenv

# account情報をaccount.pyからロード
from metamon_code import meta_manuscript


class Hometamon():
    def __init__(self, test=True):
        load_dotenv(".env")
        # AWS上では相対パスではだめ
        # load_dotenv("metamon_code/.env")
        consumer_key = os.environ.get("CONSUMER_KEY")
        consumer_secret = os.environ.get("CONSUMER_SECRET")
        access_token = os.environ.get("ACCESS_TOKEN")
        token_secret = os.environ.get("TOKEN_SECRET")

        auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
        auth.set_access_token(key=access_token, secret=token_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)
        self.my_twitter_id = os.environ.get("TWITTER_ID")
        self.manuscript = meta_manuscript.Manuscript()
        JST = datetime.timezone(datetime.timedelta(hours=+9), "JST")
        self.jst_now = datetime.datetime.now(JST)
        self.admin_twitter_id = os.environ.get("ADMIN_RECIPIENT_ID")
        # for test
        self.test = test

    def check_api(self):
        limit_info = self.api.rate_limit_status()
        dir(limit_info["rate_limit_status"])

    # read tweets
    def classify(self):
        classify_words = ["褒めて", "ほめて", "バオワ", "ばおわ", "バイト終", "バおわ", "実験終", "実験おわ", "らぼりだ", "ラボ離脱", "ラボりだ", "帰宅", "疲れた",
                          "つかれた", "仕事納め", "掃除終", "掃除した", "がこおわ", "学校終"]
        ohayou_words = ["おはよう", "起床", "起きた", "ぽきた", "おきた"]
        oyasumi_words = ["おやすみ", "寝よう", "寝る", "寝ます", "ねるね"]
        transform_commands = []
        test_command = ["_test_"]
        exclusion_names = ["bot", "ビジネス", "副業", "公式", "株", "FX", "ブランド", "無料", "キャリア", "エージェント"]
        exclusion_words = ["#peing", "http"]

        count_reply = {"ignore": 0,
                       "praise": 0,
                       "greeting_morning": 0,
                       "greeting_nignt": 0,
                       "pass": 0,
                       "test": 0}

        public_tweets = self.api.home_timeline(count=50, since_id=None)

        if self.test:
            print("#" * 10, "test", "#" * 10)
        else:
            print("#" * 10, "product", "#" * 10)

        for tweet_cnt, tweet in enumerate(public_tweets):
            user_name = tweet.user.name  # HN
            screen_name = tweet.user.screen_name  # ID
            reply_flag = True

            tweet_split = tweet.text.split(" ")
            print("")
            print(tweet_cnt, ":", end="")
            if self.test:
                print("text:", tweet.text)
                # print("char count:",len(tweet.text))
            print("reply status:", end="")

            # 自分には返事しない
            if screen_name == self.my_twitter_id:
                print("this tweet is mine")
                count_reply["ignore"] += 1
                reply_flag = False
                continue

            # ファボしたツイートには反応しない
            elif tweet.favorited:
                print("you alredy favorited")
                count_reply["ignore"] += 1
                reply_flag = False
                continue

            # RTには返事しない
            elif tweet_split[0] == "RT":
                print("this is retweeted")
                count_reply["ignore"] += 1
                reply_flag = False
                continue

            # 誰かへのツイートには返事しない
            elif tweet_split[0][0] == "@":
                print("this is to someone")
                count_reply["ignore"] += 1
                reply_flag = False
                continue

            # tweet内容が80文字を超えている場合には返事しない
            elif len(tweet.text) >= 80:
                count_reply["ignore"] += 1
                reply_flag = False
                continue

            # 上記の除外ワードを含む人には返事しない
            if reply_flag:
                for exclusion_name in exclusion_names:
                    if exclusion_name in user_name:
                        print("ignore account")
                        count_reply["ignore"] += 1
                        reply_flag = False
                        break

            # 上記の単語を含むツイートを無視する
            if reply_flag:
                for exclusion_word in exclusion_words:
                    if exclusion_word in tweet.text:
                        print("ignore this tweet")
                        count_reply["ignore"] += 1
                        reply_flag = False
                        break

            if reply_flag:
                print("this is pass")
                user_name_ = user_name.split("@")
                # 返信part
                for classify_word in classify_words:
                    if classify_word in tweet.text:
                        count_reply["praise"] += 1
                        # reply
                        self.reply(user_name_[0], screen_name, tweet.id, tweet.text)
                        # favorite
                        self.api.create_favorite(tweet.id)
                        reply_flag = False
                        break

            if reply_flag:
                # 挨拶part おはよう
                if 5 <= self.jst_now.hour <= 10:
                    for ohayou_word in ohayou_words:
                        if ohayou_word in tweet.text:
                            print("greeting_morning")
                            count_reply["greeting_morning"] += 1
                            self.greeting_morning(user_name_[0], screen_name, tweet.id, tweet.text)
                            self.api.create_favorite(tweet.id)
                            reply_flag = False
                            break

                # 挨拶　おやすみ
                if 22 <= self.jst_now.hour or self.jst_now.hour <= 2:
                    for oyasumi_word in oyasumi_words:
                        if oyasumi_word in tweet.text:
                            print("good night")
                            count_reply["greeting_nignt"] += 1
                            self.greeting_nignt(user_name_[0], screen_name, tweet.id, tweet.text)
                            self.api.create_favorite(tweet.id)
                            reply_flag = False
                            break

            if reply_flag:
                # 変身part
                for transform_command in transform_commands:
                    if transform_command in tweet.text:
                        # transform
                        self.transform()
                        self.api.create_favorite(tweet.id)
                        reply_flag = False
                        break

                # test part
                if test_command[0] in tweet.text:
                    if screen_name == "yosyuaomenww":
                        self.test_tweet()
                        self.api.create_favorite(tweet.id)
                        print("test tweet")
                        reply_flag = False

                        break

            if reply_flag:
                count_reply["pass"] += 1

        if self.test:
            mode = "test"
        else:
            mode = "deploy"

        result = "time:{0}\nmode:{1}\n褒めた数:{2}\n無効な数:{3}\n挨拶した数:{4}\n反応しなかった数:{5}\nテスト数:{6}だもん！！".format(
            str(self.jst_now),
            mode,
            count_reply["praise"],
            count_reply["ignore"],
            count_reply["greeting_morning"] + count_reply["greeting_nignt"],
            count_reply["pass"],
            count_reply["test"])
        print(result)
        # 自分のアカウントにDMを送信
        self.api.send_direct_message(self.admin_twitter_id, result)

    # 返事をする
    def reply(self, user_name, screen_name, tweet_id, tweet_text):
        num = random.randint(0, len(self.manuscript.reply) - 1)
        # num_padded = '{0:03d}'.format(num) #ゼロパディング:0で３桁左詰する。 example 1→001
        print(num)
        reply = "@" + screen_name + "\n " + user_name + self.manuscript.reply[num]
        if self.test:
            print("-----test:reply-----")
        else:
            self.api.update_status(status=reply, in_reply_to_status_id=tweet_id)  # status
        print("tweet:{0}:{1} \nreply:{2}".format(user_name, tweet_text, reply))

    def greeting_morning(self, user_name, screen_name, tweet_id, tweet_text):
        num = random.randint(0, len(self.manuscript.greeting_morning) - 1)
        reply = "@" + screen_name + "\n " + user_name + self.manuscript.greeting_morning[num]
        if self.test:
            print("-----test:greeting_morning-----")
        else:
            self.api.update_status(status=reply, in_reply_to_status_id=tweet_id)  # status
        print("tweet:{0}:{1} \nreply:{2}".format(user_name, tweet_text, reply))

    def greeting_nignt(self, user_name, screen_name, tweet_id, tweet_text):
        num = random.randint(0, len(self.manuscript.greeting_night) - 1)
        reply = "@" + screen_name + "\n " + user_name + self.manuscript.greeting_night[num]
        if self.test:
            print("-----test:greeting_night-----")
        else:
            self.api.update_status(status=reply, in_reply_to_status_id=tweet_id)
        print("tweet:{0}:{1} \nreply:{2}".format(user_name, tweet_text, reply))

    # フォロバする
    def followback(self):
        if self.test:
            print("-----test:followback-----")
        else:
            # 最近のフォロワーからその人のtweetやid情報取得
            followers = self.api.followers_ids(self.my_twitter_id)
            friends = self.api.friends_ids(self.my_twitter_id)

            follow_back = list(set(followers) - set(friends))  # list フォロバすべき
            print("フォローバックしたい人数:{0}人".format(len(follow_back)))

            random.shuffle(follow_back)

            follow_back = follow_back[:10]
            user_statuses = self.api.lookup_users(follow_back)
            for status in user_statuses:
                if status.follow_request_sent:
                    print("I already request to follow")
                else:
                    try:
                        self.api.create_friendship(id=status.id)
                        print("success follow!" + str(status.screen_name))
                    except tweepy.error.TweepError as e:
                        print(e)
                        print("error")

    def tweet(self):
        status = "順調だもん!"
        self.api.update_status(status=status)

    def transform(self):
        pass
        # status = "変身だもん"
        # self.api.update_status(status=status)

    def test_tweet(self):
        if self.test:
            status = "zzz"
        else:
            status = "起きてるもん！\n⊂・ー・つ"
        self.api.update_status(status=status)
        print(status, "とツイートしました．")

    def get_user_info(self):
        user_info = self.api.get_user(self.my_twitter_id)
        print(user_info)

    def check_timeline(self):
        since = None
        public_tweets = self.api.home_timeline(count=10, since_id=since)
        print(self.my_twitter_id)

        for tweet in public_tweets:
            print("-" * 20)
            # print(tweet)
            print(tweet.text)
            # RTには返事しない
            tweet_split = tweet.text.split(" ")
            if tweet_split[0] == "RT":
                reply_flag = True
                print("this is retweeted")
            elif tweet_split[0][0] == "@":
                reply_flag = True
                print("this is to someone")
            else:
                print("this is original")

            if tweet.user.screen_name == self.twitter_id:
                print("-" * 10)
                print(tweet.user.name, tweet.user.screen_name, "\n", tweet.text)
            # print(tweet.user.name,tweet.user.screen_name)


def main(test):
    # test command
    hometamon = Hometamon(test)
    # hometamon.check_api()
    # hometamon.get_user_info()
    # """
    hometamon.classify()
    hometamon.followback()
    # """


def lambda_handler(event, context):
    main(test=False)
    # hometamon = Hometamon()
    # hometamon.check_timeline()


if __name__ == "__main__":
    # main(test = False)
    main(test=True)
    # hometamon = Hometamon()
    # hometamon.check_timeline()
