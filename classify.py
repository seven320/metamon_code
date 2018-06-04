#encoding:utf-8
import tweepy
import reply
#親ディレクトリにあるアカウント情報へのパス
import sys,os
pardir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)

#account情報をaccount.pyからロード
from account import account #load account
auth=account.Initialize()
api = tweepy.API(auth)
twitter_id=account.id()

classify_list=["褒めて","ほめて","承認","讃えて","たたえて"]

public_tweets = api.home_timeline(count=10)



for tweet in public_tweets:
    user_name=tweet.user.name
    screen_name=tweet.user.screen_name#@以下のID
    tweet_id=tweet.id
    tweet_text=tweet.text
    for i in range(len(classify_list)):
        if classify_list[i] in tweet_text:
            print("test:承認")
            reply.main(user_name,screen_name,tweet_id,tweet_text)
        else:
            print("test:非承認")
