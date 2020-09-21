# encoding: utf-8

import json 
import requests
from datetime import datetime as dt
import datetime
import random
import traceback
import os, sys

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)

from src import meta_manuscript 
from src import hometamon
from src import tweet_intent

"""
DjangoのサーバーとCRUDを行う．
"""
headers = {'Content-Type':'application/json'}
manuscript = meta_manuscript.Manuscript()

class API():
    def __init__(self):
        # local
        # self.base_url = "http://localhost:8001/api"
        # dokcer
        self.base_url = "http://hometask:8001/api"

    def get_user(self, user_id):
        url = self.base_url + "/users/{}/".format(user_id)
        response = requests.get(url, headers = headers)
        return response

    def post_user(self, user_name, user_id, screen_name, secret_status):
        if secret_status:
            secret_status = "1"
        else:
            secret_status = "0"
        data = {
            "user_name": user_name,
            "user_id": user_id,
            "screen_name": screen_name,
            "secret_status": secret_status
        }
        url = self.base_url + "/users/"

        response = requests.post(url, data = json.dumps(data), headers = headers)
        print(response)
        return response

    def post_task(self, task, user_id):
        data = {
            "task": task,
            "user_id": user_id
        }
        url = self.base_url + "/tasks/"

        response = requests.post(url, data = json.dumps(data), headers = headers)

        return response

    def post_task_history(self, tweet_id, tweet_text, user_id, task_id):
        data = {
            "tweet_id": tweet_id,
            "tweet_text": tweet_text,
            "user_id": user_id,
            "task_id": task_id
        }
        url = self.base_url + "/task_historys/"

        response = requests.post(url, data = json.dumps(data), headers = headers)
        return response

    def search_task(self, user_id):
        url = self.base_url + "/search/tasks/?user_id={}".format(user_id)
        response = requests.get(url)
        return response

    def search_task_history(self, user_id):
        url = self.base_url + "/search/task_historys/?user_id={}".format(user_id)
        response = requests.get(url)
        return response

    def set_user(self, user):
        r = self.get_user(user.id)
        if r.status_code != 200:# user登録されてない
            print("set user")
            try:
                r = self.post_user(user.name, user.id, user.screen_name, user.protected)
            except:
                traceback.print_exc()
                return False
            if r.status_code != 201:
                print("error:", r.json)
                return False
        return True

    # task登録が来た時に行う
    def set_task(self, user, task):
        if self.set_user(user) == False:
            return False
        try:
            r = self.post_task(task, user.id)
        except:
            traceback.print_exc()
            return False
        if r.status_code != 201:
            print("error: post_task", r.status_code)
            return False
        return True

    def set_task_history(self, tweet_id, tweet_text, user_id):
        r = self.search_task(user_id = user_id)
        if r.status_code != 200:
            print("error:", r.content)
            return False
        tasks = json.loads(r.content)["results"]
        try: 
            task_id = tasks[-1]["id"]
        except: # taskが存在してないとき
            traceback.print_exc()
            return False
        try:
            r = self.post_task_history(tweet_id, tweet_text, user_id, task_id)
            traceback.print_exc()
        except:
            tryceback.print_exc()
            return False
        if r.status_code != 201:
            return False
        return True

class HomeTask(hometamon.Hometamon):
    def __init__(self):
        super().__init__()
        self.task_words = ["#hometask"]
        self.django_api = API()

    def check_task(self, tweet):
        if not "@denden_by" in tweet.text:
            return False
        if self.set_task_words[0] in tweet.text:
            return True
        return False

    def check_task_history(self, tweet):
        if "#hometask" in tweet.text:
            return True
        return False

    def extract_task(self, tweet_text):
        task = tweet_text.replace("@denden_by","").replace("\n", "").replace(" ", "").replace(":", "").replace("：", "")
        for set_task_word in self.set_task_words:
            task = task.replace(set_task_word, "")
        return task

    def set_task_and_reply(self, tweet):
        task = self.extract_task(tweet.text)
        if self.django_api.set_task(tweet.user, task):
            intent_url = tweet_intent.make(text = "", hashtag = "hometask")
            reply = "@" + tweet.user.screen_name + "\n" + "{}を覚えたもん！今日から頑張るもん!!\n報告は #hometask をつけてもん!!\n{}\n".format(task, intent_url)
        else:
            reply = "@" + tweet.user.screen_name + "\n" + "うまく覚えれなかったもん\nごめんなさいもん"
        self.api.update_status(status = reply, in_reply_to_status_id = tweet.id)
        self.api.create_favorite(tweet.id)
        return reply

    def set_task_history_and_reply(self, tweet):
        if self.django_api.set_task_history(tweet.id, tweet.text, tweet.user.id):
            reply = self.make_reply(user_id = tweet.user.id)
        else:
            reply = "まだtaskが設定されてないもん!!下のurlからツイートして設定するもん."
            reply = reply + "\n" + tweet_intent.make(text = "settask:", tweet_to="denden_by")
        reply = "@" + tweet.user.screen_name + "\n" + self.user_name_changer(tweet) + reply
        self.api.update_status(status = reply, in_reply_to_status_id = tweet.id)
        self.api.create_favorite(tweet.id)
        return reply

    def classify_reply(self, user_id):
        # user_idに基づくので，taskを変更してもしなくても関係ない．
        r = self.django_api.search_task_history(user_id)
        if r.status_code != 200:
            return "", None
        count = r.json()["count"]
        task_historys = r.json()["results"]
        streak_count = self.count_hometask_streak(task_historys)
        if streak_count in list(self.manuscript.streak_reply.keys()):
            return self.praised_streak(streak_count), count
        if count in list(self.manuscript.icon.keys()):
            return self.praised_count_hometask(count), count
        return self.praised_random(), count

    def make_icon(self, count):
        icons = self.manuscript.icon
        icon = ""
        for key in icons.keys():
            if count >= key:
                icon = icons[key]
        return chr(int(icon, 16))

    def make_reply(self, user_id):
        reply, count = self.classify_reply(user_id)
        if count == None:
            print("count is None")
        reply = self.make_icon(count) + reply
        return reply 

    # 各種のreply
    def praised_random(self):
        reply = random.choice(self.manuscript.hometask_random_reply)
        return reply

    def praised_count_hometask(self, count):
        reply = self.manuscript.count_reply[count]
        reply = reply + self.make_icon(count)
        return reply

    def praised_streak(self, streak_count):
        reply = self.manuscript.streak_reply[streak_count]
        return reply    
    
    def count_hometask_streak(self, task_historys):
        # 現在のstreakを計算する
        reversed_task_historys = list(reversed(task_historys))
        streak_count = 0
        newest_created_at = dt.strptime(reversed_task_historys[0]["created_at"],"%Y-%m-%dT%H:%M:%S.%f").date()
        pre_created_at = newest_created_at
        for i, task in enumerate(reversed_task_historys):
            created_at = dt.strptime(task["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
            if pre_created_at - datetime.timedelta(days=1) > created_at.date():
                break
            pre_created_at = created_at.date()
        streak_count = (newest_created_at - pre_created_at).days + 1
        return streak_count

    def hometask_exclude(self, tweet):
        if str(tweet.user.id) == self.my_twitter_user_id:
            return True
        elif tweet.favorited:
            return True
        elif tweet.text.split(" ")[0] == "RT":
            return True
        elif tweet.text.split(" ")[0][0] == "@":
            if "@denden_by" in tweet.text:
                if self.set_task_words[0] in tweet.text:
                    return False
                if self.task_words[0] in tweet.text:
                    return False
                self.api.create_favorite(id = tweet.id)
            return True
        return False  

def main():
    ht = HomeTask()
    public_tweets = ht.get_tweets()
    for tweet in public_tweets:
        if ht.hometask_exclude(tweet):
            pass
        else:
            if ht.check_task(tweet): # set taskをする
                print("settask")
                reply = ht.set_task_and_reply(tweet)
            elif ht.check_task_history(tweet): # hometask
                print("set task_history")
                reply = ht.set_task_history_and_reply(tweet)

if __name__ == "__main__":
    print("te")
    main()
