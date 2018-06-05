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

def main():
    twitter_id=account.id()
    since_id=None

    classify_list=["褒めて","ほめて","承認","讃えて","たたえて","返信","変身"]

    public_tweets = api.home_timeline(count=10,since_id=since_id)
    #
    # print(len(public_tweets))
    # print(type(public_tweets))
    # print(public_tweets[-1])
    # print(public_tweets[1])

    for tweet in public_tweets:
        user_name=tweet.user.name#HN
        screen_name=tweet.user.screen_name#@以下のID
        tweet_id=tweet.id
        tweet_text=tweet.text
        for i in range(len(classify_list)):
            if classify_list[i] in tweet_text:
                if tweet.favorited==False:
                    print("test:承認")
                    # #reply
                    reply.main(user_name,screen_name,tweet_id,tweet_text)
                    # #favorite
                    api.create_favorite(tweet_id)
                else:print("you already reply it!!")
            else:
                print("test:非承認")

if __name__=="__main__":
    main()
