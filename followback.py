#encoding:utf-8
# 参照url
# https://qiita.com/yuki_bg/items/96a1608aa3f3225386b6
# http://tweepy.readthedocs.io/en/v3.5.0/api.html#API.update_status

import certifi
import tweepy

#親ディレクトリにあるアカウント情報へのパス
import sys,os
pardir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)

#account情報をaccount.pyからロード
from account import account #load account
auth=account.Initialize()
api = tweepy.API(auth)
twitter_id=account.id()

#最近のフォロワーからその人のtweetやid情報取得
# followers=api.followers_ids(screen_name=twitter_id)#全てのフォロワーidを取得
# friends=api.friends_ids(twitter_id)#フォローしている人のidを取得
followers=api.followers_ids(twitter_id)
friends=api.friends_ids(twitter_id)

# following
# for follower in followers['users']:
#     name=follower['screen_name']
#     print(name)
#     if follower['following'] or follower['follow_request_sent']:#if follow that follower or sent follow request, pass that follower
#         pass
#     else:#フォローしてないときはフォロー申請 if i dont follow that follower, request following
#         # t.friendships.create(screen_name=name)
#         pass
# print(followers)
#フォロワーからフォローしている人を引く
list_followback=list(set(followers)-set(friends))#フォローバックすべき一覧
print("list_followback,count=",len(list_followback))

#follow back-part
#num of follow once
count=10
if count>len(list_followback):
    count=len(list_followback)

for follownum in range(count):
    # follow-part
    try:
        api.create_friendship(list_followback[follownum])
        print("success follow!"+str(list_followback[follownum]))
    except tweepy.error.TweepError:
        print("Error: You've already requested to follow")
