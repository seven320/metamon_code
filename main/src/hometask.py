# encoding: utf-8

import json 
import requests
from datetime import datetime as dt
import datetime
import random

from src import meta_manuscript 

"""
DjangoのサーバーとCRUDを行う．
"""
headers = {'Content-Type':'application/json'}
manuscript = meta_manuscript.Manuscript()

class API():
    def __init__(self):
        self.base_url = "http://localhost:8001/api"

    def get_user(self, user_id):
        url = self.base_url + "/users/{}".format(user_id)
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
        print(response.json)
        print(response.content)
        return response

    def search_task(self, user_id):
        url = self.base_url + "/search/tasks/?user_id={}".format(user_id)
        response = requests.get(url)
        return response

    def search_task_history(self, user_id):
        url = self.base_url + "/search/task_historys/?user_id={}".format(user_id)
        response = requests.get(url)
        print(response.json)
        print(response.content)
        return response

    def set_user(self, user):
        r = self.get_user(user.id)
        if r.status_code != 200:# user登録されてない
            r = post_user(user.name, user.id, user.screen_name, secret_status = user.protected)
            if r.status_code != 201:
                print("error:", r.json)
                return False
        return True

    # task登録が来た時に行う
    def set_task(self, user, task):
        if self.set_user(user) == False:
            return False
        r = self.post_task(task, user.id)
        if r.status_code != 201:
            return False
        return True

    def set_task_history(self, tweet_id, tweet_text, user_id):
        r = self.search_task(user_id = user_id)
        if r.status_code != 200:
            print("error:", r.content)
            return False
        tasks = json.loads(r.content)["results"]
        print(tasks)
        try: 
            task_id = tasks[-1]["id"]
        except: # taskが存在してないとき
            return False
        r = self.post_task_history(tweet_id, tweet_text, user_id, task_id)
        if r.status_code != 201:
            return False
        return True

def count_hometask_streak(task_historys):
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

api = API()

"""
make reply
"""

def classify_reply(user_id, manuscript = manuscript, api = api):
    # user_idに基づくので，taskを変更してもしなくても関係ない．
    r = api.search_task_history(user_id)
    if r.status_code != 200:
        return "", None
    data = json.loads(r.content)
    count = data["count"]
    task_historys = data["results"]

    streak_count = count_hometask_streak(task_historys)
    if streak_count in list(manuscript.streak_reply.keys()):
        return praised_streak(streak_count), count
    if count in list(manuscript.icon.keys()):
        return praised_count_hometask(count), count
    return praised_random(), count

def make_icon(count, manuscript = manuscript):
    icons = manuscript.icon
    icon = ""
    for key in icons.keys():
        if count >= key:
            icon = icons[key]
    return chr(int(icon, 16))

def make_reply(user_id):
    reply, count = classify_reply(user_id)
    if count == None:
        print("count is None")
    icon = make_icon(count)
    reply = icon + reply
    return reply 

# reply
def praised_random(manuscript = manuscript):
    reply = random.choice(manuscript.hometask_random_reply)
    return reply

def praised_count_hometask(count, manuscript = manuscript):
    reply = manuscript.count_reply[count]
    reply = reply + make_icon(count)
    return reply

def praised_streak(streak_count, manuscript = manuscript):
    reply = manuscript.streak_reply[streak_count]
    return reply
