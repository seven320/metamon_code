#encoding:utf-8
import tweepy

#親ディレクトリにあるアカウント情報へのパス
import sys,os
pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)

#account情報をaccount.pyからロード
from account import account #load account
auth = account.Initialize()
api = tweepy.API(auth)
twitter_id = account.id()

import meta_manuscript
#原稿のロードのためにclass継承　from manuscript.py
tweet = meta_manuscript.Manuscript()

# 指定された写真の範囲からランダムに選ぶ
import random
min = 1
max = tweet.max_num()#記事の割り振り番号の最大値
num = random.randint(min,max)
num_padded = '{0:03d}'.format(num)#ゼロパディング:0で３桁左詰する。 example 1→001

# ツイートのみ
def main(user_name,screen_name,tweet_id,tweet_text):
    reply="@"+screen_name+"\n "+user_name+tweet.manus(num-1)
    api.update_status(status = reply, in_reply_to_status_id=tweet_id)#status
    print("{0}のツイート:{1} に{2}と応援しました!".format(user_name,tweet_text,reply))
