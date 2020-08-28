# encoding: utf-8

import json 
import requests

"""
DjangoのサーバーとCRUDを行う．
"""

base_url = "http://localhost:8001/api"
headers = {'Content-Type':'application/json'}


# get user
def get_user(user_id):
    url = base_url + "/users/{}".format(user_id)

    response = requests.get(url, headers = headers)
    print(response.content)

# POST USER
def post_user(user_name, user_id, screen_name, secret_status):
    if secret_status:
        secret_status = "secret"
    else:
        secret_status = "public"
    data = {
        "user_name": user_name,
        "user_id": user_id,
        "screen_name": screen_name,
        "secret_status": secret_status
    }
    url = base_url + "/users/"

    response = requests.post(url, data = json.dumps(data), headers = headers)

    print(response.content)
    print(response.headers)
    print(response.json)

def post_task(task, user_id):
    data = {
        "task": task,
        "user_id": user_id
    }
    url = base_url + "/tasks/"

    response = requests.post(url, data = json.dumps(data), headers = headers)
    print(response.json)
    print(response.content)

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

def search_task_history(task_id):
    url = base_url + "/search/task_historys/?task_id={}".format(task_id)
    response = requests.get(url)
    print(response.json)
    print(response.content)

if __name__ == "__main__":
    # post_user(user_name="hoge", user_id = 1222, screen_name = "yo", secret_status = 1)
    # post_task(task = "hoge", user_id = 12)

    # set
    # post_task_history(tweet_id = 12345, tweet_text = "done hoge", user_id = "12", task_id = 4)
    # search_task_history(task_id = 4)
    get_user(user_id = 123)



"""
get_user
post_user

post_task


post_task_history

"""