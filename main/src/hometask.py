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

base_url = "http://localhost:8001/api"
headers = {'Content-Type':'application/json'}
manuscript = meta_manuscript.Manuscript()

def get_user(user_id):
    url = base_url + "/users/{}".format(user_id)
    response = requests.get(url, headers = headers)
    return response

def post_user(user_name, user_id, screen_name, secret_status):
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
    url = base_url + "/users/"

    response = requests.post(url, data = json.dumps(data), headers = headers)
    return response

def post_task(task, user_id):
    data = {
        "task": task,
        "user_id": user_id
    }
    url = base_url + "/tasks/"

    response = requests.post(url, data = json.dumps(data), headers = headers)

    return response

def post_task_history(tweet_id, tweet_text, user_id, task_id):
    data = {
        "tweet_id": tweet_id,
        "tweet_text": tweet_text,
        "user_id": user_id,
        "task_id": task_id
    }
    url = base_url + "/task_historys/"

    response = requests.post(url, data = json.dumps(data), headers = headers)
    print(response.json)
    print(response.content)
    return response

def search_task(user_id):
    url = base_url + "/search/tasks/?user_id={}".format(user_id)
    response = requests.get(url)
    return response

def search_task_history(user_id):
    url = base_url + "/search/task_historys/?user_id={}".format(user_id)
    response = requests.get(url)
    print(response.json)
    print(response.content)
    return response

def set_user(user):
    r = get_user(user.id)
    if r.status_code != 200:# user登録されてない
        r = post_user(user.name, user.id, user.screen_name, secret_status = user.protected)
        if r.status_code != 201:
            print("error:", r.json)
            return False
    return True

# task登録が来た時に行う
def set_task(user, task):
    if set_user(user) == False:
        return False
    r = post_task(task, user.id)
    if r.status_code != 201:
        return False
    return True

def set_task_history(tweet_id, tweet_text, user_id):
    r = search_task(user_id = user_id)
    if r.status_code != 200:
        print("error:", r.content)
        return False
    tasks = json.loads(r.content)["results"]
    print(tasks)
    task_id = tasks[-1]["id"]

    r = post_task_history(tweet_id, tweet_text, user_id, task_id)
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
def make_reply(user_id):
    # user_idに基づくので，taskを変更してもしなくても関係ない．
    r = search_task_history(user_id)
    if r.status_code != 200:
        return ""
    data = json.loads(r.content)
    count = data["count"]
    task_historys = data["results"]
    streak_count = count_hometask_streak(task_historys)
    if streak_count in [3, 7, 14, 21, 28]:
        return praised_streak(streak_count)
    if count in [1, 5]:
        return praised_count_hometask(count)
    return praised_random()

# reply
def praised_random():
    reply = random.choice(manuscript.reply)
    # if random.random() > 0.3:
    #     "\nこれ拾ったもん!!!あげるもん!!!\nつ{}".format(random.choice(manuscript.rewards))
    return reply

def praised_count_hometask(count):
    if count == 1:
        reply = "最初の達成だもんね．偉いもん！！称号あげるもん\nつ🐣"
    elif count == 5:
        reply = "#hometask 5回目だもん，すごいもん!!これあげるもん!!!\nつ🐔"
    return reply

def praised_streak(streak_count):
    if streak_count == 3:
        reply = "連続3日達成だもん!!!すごいもん!!これあげるもん\nつ🌟"
    elif streak_count == 7:
        reply = "連続7日hometask達成だもん!!!この調子で続けるもん!!\n銅メダルあげるもん!\nつ🥉"
    elif streak_count == 14:
        reply = "連続14日hometask達成だもん!!偉いもん!!\n銀メダルあげるもん\nつ🥈"
    elif streak_count == 21:
        reply = "連続21日達成だもん!!すごいもん!!!誇っていいもんよ!!!\n金メダルあげるもん\nつ🥇"
    elif streak_count == 28:
        reply = "連続28日達成だもん偉いもん．\nトロフィーあげるもん!!!\nつ🏆"
    return reply



