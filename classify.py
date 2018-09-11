#encoding:utf-8
import tweepy

#親ディレクトリにあるアカウント情報へのパス
import sys,os
pardir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)

from metamon_code import reply
#account情報をaccount.pyからロード
from account import account #load account
auth=account.Initialize()
api = tweepy.API(auth)

def lambda_handler():
    twitter_id = account.id()
    since_id = None
    test_word = "_test_"
    classify_list = ["褒めて","ほめて","讃えて","たたえて","えらい"]
    transform_command = ["褒めたもん変身"]

    public_tweets = api.home_timeline(count=50,since_id=since_id)
    #
    # print(len(public_tweets))
    # print(type(public_tweets))
    # print(public_tweets[-1])
    # print(public_tweets[1])

    for tweet in public_tweets:
        #HNに対する処理
        user_name = tweet.user.name#HN
        #user_nameについて@以下の情報を削除
        user_name = user_name.split("@")

        screen_name=tweet.user.screen_name#@以下のID
        tweet_id=tweet.id
        tweet_text=tweet.text

        #for_test
        if test_word in tweet_text:
                print("test:test用コマンド承認")
                #reply
                reply.main(user_name[0],screen_name,tweet_id,tweet_text)

        for i in range(len(classify_list)):
            if classify_list[i] in tweet_text:
                if tweet.favorited == False:
                    print("test:承認")
                    #reply
                    reply.main(user_name[0],screen_name,tweet_id,tweet_text)
                    #favorite
                    api.create_favorite(tweet_id)
                else:print("you already reply it!!")
            else:
                print("test:非承認")
        #裏コマンド　変身
        # for j in range(len(transform_command)):
        #     if transform_command in tweet_text:
        #         if tweet.favorited==False:
        #             api.
        #             # #favorite
        #             api.create_favorite(tweet_id)
        #         else:print("変身済みです")


if __name__=="__main__":
    lambda_handler()
