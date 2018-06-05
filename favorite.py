#encoding:utf-8
# 参照url
#https://syncer.jp/Web/API/Twitter/REST_API/POST/statuses/update/
#http://ailaby.com/twitter_api/
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

#get timeline
public_tweets = api.home_timeline(count=5)
# print(public_tweets[0])
print("取得ツイート数："+str(len(public_tweets)))

for tweet in public_tweets:#複数形と単数形でしか対応しない
    print("\n"+tweet.text)
    print("\nfavorite count:"+str(tweet.favorite_count))
    print("retweet count:"+str(tweet.retweet_count))
    if 0<(int(tweet.favorite_count)+int(tweet.retweet_count)*2)<5:
        if tweet.favorited==False:
            print("favorite it!")
            #favorite

            api.create_favorite(tweet.id)
            pass
        else:
            print("I already favorited it")
    else:
        print("This tweet doesn't suit your rules")
