# encoding utf-8
import os, sys
import random 
import datetime as dt

import tweepy

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)

from src import meta_manuscript
from dotenv import load_dotenv


class Hometamon():
    def __init__(self):
        if os.path.exists(".env"):
            load_dotenv(".env")
        elif os.path.exists("src/.env"):
            load_dotenv("src/.env")
        elif os.path.exists("/src/.env"):
            load_dotenv("/src/.env")
        elif os.path.exists("main/src/.env"):
            load_dotenv("main/src/.env")
        elif os.path.exists("../src/.env"):
            load_dotenv("../src/.env")
        else:
            print("error doesn't exist .env path")

        consumer_key = os.environ.get("CONSUMER_KEY")
        consumer_secret = os.environ.get("CONSUMER_SECRET")
        access_token = os.environ.get("ACCESS_TOKEN")
        token_secret = os.environ.get("TOKEN_SECRET") 

        auth = tweepy.OAuthHandler(
            consumer_key = consumer_key,
            consumer_secret = consumer_secret)
        auth.set_access_token(
            key = access_token,
            secret = token_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit = True)
        self.my_twitter_id = os.environ.get("TWITTER_ID")
        self.manuscript = meta_manuscript.Manuscript()
        JST = dt.timezone(dt.timedelta(hours=+9), "JST")
        self.JST = dt.datetime.now(JST)
        self.admin_twitter_id = os.environ.get("ADMIN_RECIPIENT_ID")

        self.exclusion_user_names = ["bot", "ビジネス", "副業", "公式", "株", "FX", "ブランド", "無料", "キャリア", "エージェント"] # user name
        self.exclusion_words = ["peing", "http"]
        self.greeting_morning_words = ["おはよう", "ぽきた", "起きた", "起床", "早起き"]
        self.greeting_nighy_words = ["おやすみ", "寝よう", "寝る", "寝ます"]
        self.classify_words = [
            "褒めて", "ほめて",
            "バオワ", "ばおわ", "バイト終", "バおわ", 
            "実験終", "実験おわ", "らぼりだ", "ラボ離脱", "ラボりだ", 
            "帰宅", "帰る", "疲れた","つかれた", 
            "仕事納め", "仕事した",
            "掃除終", "掃除した", "がこおわ", "学校終"]
        self.set_task_words = ["settask", "設定"]
        self.task_words = ["#hometask"]
        self.transform_words = ["変身"]
        self.test_words = ["__test__"]

        self.counts = {
            "ignore": 0,
            "praise": 0,
            "greeting_morning": 0,
            "greeting_night": 0,
            "pass": 0,
            "transform": 0,
            "test": 0
        }

    def get_tweets(self):
        return self.api.home_timeline(count = 100, since_id = None)

    def user_name_changer(self, tweet):
        user_name = tweet.user.name
        if "@" in user_name:
            user_name = user_name.split("@")[0]
        elif  "＠" in user_name:
            user_name = user_name.split("＠")[0]
        return user_name

    def greeting_morning(self, tweet):
        reply = "@" + tweet.user.screen_name + "\n" + self.user_name_changer(tweet) + random.choice(self.manuscript.greeting_morning)
        self.counts["greeting_morning"] += 1
        self.api.update_status(status = reply, in_reply_to_status_id = tweet.id)
        self.api.create_favorite(tweet.id)
        return reply
    
    def greeting_night(self, tweet):
        reply = "@" + tweet.user.screen_name + "\n" + self.user_name_changer(tweet)  + random.choice(self.manuscript.greeting_night)
        self.counts["greeting_night"] += 1
        self.api.update_status(status = reply, in_reply_to_status_id = tweet.id)
        self.api.create_favorite(tweet.id)
        return reply

    def praise(self, tweet):
        reply = "@" + tweet.user.screen_name + "\n" + self.user_name_changer(tweet)  + random.choice(self.manuscript.reply)
        self.counts["praise"] += 1
        self.api.update_status(status = reply, in_reply_to_status_id = tweet.id)
        self.api.create_favorite(tweet.id)
        return reply

    def tweet_sweet(self):
        status = random.choice(self.manuscript.sweet_tweet_before)
        status += "\n⊂・ー・つ" + chr(int(random.choice(self.manuscript.sweets)[2:], 16)) + "\n" # 16進数から変換
        status += random.choice(self.manuscript.sweet_tweet_after)
        self.api.update_status(status = status)

    def test_tweet(self):
        status = "起きてるもん！\n⊂・ー・つ"
        self.api.update_status(status = status)
        self.counts["test"] += 1
        return status

    def check_exclude(self, tweet): # 除外するかどうかcheck
        if tweet.user.name == self.my_twitter_id:
            return True        
        elif tweet.favorited:
            return True
        elif tweet.text.split(" ")[0] == "RT":
            return True
        elif tweet.text.split(" ")[0][0] == "@":
            if "@denden_by" in tweet.text and not "task" in tweet.text:# 自分へのreplyへはファボし，taskはここではpass
                self.api.create_favorite(id = tweet.id)
                return True
        elif len(tweet.text) >= 80: # if tweet is more than 80 words, it will be ignored
            return True
        for exclusion_name in self.exclusion_user_names:
            if exclusion_name in tweet.user.name:
                return True
        for exclusion_word in self.exclusion_words:
            if exclusion_word in tweet.text:
                return True
        return False

    def check_greeting_morning(self, tweet): # 返事するかどうかcheck
        if 5 <= self.JST.hour <= 10:
            for greeting_morning_word in self.greeting_morning_words:
                if greeting_morning_word in tweet.text:
                    return True
        return False

    def check_greeting_night(self, tweet):
        if 22 <= self.JST.hour or self.JST.hour <= 2:
            for greeting_night_word in self.greeting_nighy_words:
                if greeting_night_word in tweet.text:
                    return True
        return False

    def check_sweet(self):
        return self.JST.hour == 15 and 0 <= self.JST.minute <= 5

    def check_reply(self, tweet):
        for classify_word in self.classify_words:
            if classify_word in tweet.text:
                return True
        return False

    def check_transform(self, tweet):
        for transform_word in self.transform_words:
            if transform_word in tweet.text:
                return True
        return False

    def check_test(self, tweet):
        for test_word in self.test_words:
            if tweet.user.screen_name == "yosyuaomenww" and test_word in tweet.text:
                return True
        return False

    def check_task(self, tweet):
        if not "@denden_by" in tweet.text:
            return False
        for set_task_word in self.set_task_words:
            if set_task_word in tweet.text:
                return True
        return False
    
    

    # def set_task(self, tweet):
    #     """
    #     DBへの登録を行う．まだ
    #     return [True, False]
    #     DBへの登録がうまくいけばTrue,を返す
    #     """
    #     return True

    # task を取り出す
    def extract_task(self, tweet_text):
        task = tweet_text.replace("@denden_by","").replace("\n", "").replace(" ", "").replace(":", "").replace("：", "")
        for set_task_word in self.set_task_words:
            task = task.replace(set_task_word, "")
        return task

    def set_task_reply(self, tweet):
        task = self.extract_task(tweet.text)
        reply = "@" + tweet.user.screen_name + "\n" + "{}を覚えたもん！今日から頑張るもん！！".format(task)
        self.api.update_status(status = reply, in_reply_to_status_id = tweet.id)
        self.api.create_favorite(tweet.id)
        return reply
    
    def classify(self, tweet):
        reply = ""
        if self.check_exclude(tweet):
            self.counts["ignore"] += 1
        else:
            if self.check_greeting_morning(tweet):
                reply = self.greeting_morning(tweet)
            elif self.check_greeting_night(tweet):
                reply = self.greeting_night(tweet)
            elif self.check_task(tweet):
                reply = self.set_task_reply(tweet)
            elif self.check_reply(tweet):
                reply = self.praise(tweet)
            elif self.check_transform(tweet):
                reply = self.transform()
            elif self.check_test(tweet):
                reply = self.test_tweet()
            else:
                self.counts["pass"] += 1
        return reply

    def transform(self):
        self.counts["transform"] += 1
        return ""

    def followback(self):
        followers = self.api.followers_ids(self.my_twitter_id)
        friends = self.api.friends_ids(self.my_twitter_id)
        follow_back = list(set(followers) - set(friends))
        random.shuffle(follow_back)
        user_statuses = self.api.lookup_users(follow_back[:10])
        for user_status in user_statuses:
            if user_status.follow_request_sent:
                pass
            else:
                try:
                    self.api.create_friendship(id = user_status.id)
                except tweepy.error.TweepError as e:
                    print(e)

    def report(self):
        result = "time:{}\n褒めた数:{}\n除外した数:{}\n挨拶した数:{}\n反応しなかった数:{}\n変身:{}\nテスト数:{}\n合計:{}だもん！".format(
            self.JST.strftime("%Y/%m/%d %H:%M:%S"),
            self.counts["praise"],
            self.counts["ignore"],
            self.counts["greeting_morning"] + self.counts["greeting_night"],
            self.counts["pass"],
            self.counts["transform"],
            self.counts["test"],
            sum(self.counts.values()))
        self.api.send_direct_message(self.admin_twitter_id, result)
        print(result)
        return result

def main():
    hometamon = Hometamon()
    public_tweets = hometamon.get_tweets()
    for public_tweet in public_tweets:
        hometamon.classify(public_tweet)
    if hometamon.check_sweet():
        hometamon.tweet_sweet()
    hometamon.followback()
    hometamon.report()

if __name__ == "__main__":
    main()
