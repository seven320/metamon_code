#encoding utf-8

import datetime
import tweepy
import random

#親ディレクトリにあるアカウント情報へのパス
import sys,os
pardir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)

#account情報をaccount.pyからロード
from account import account #load account
import meta_manuscript

class Hometamon():
    def __init__(self):
        auth = account.Initialize()
        self.api = tweepy.API(auth, wait_on_rate_limit=True)
        self.twitter_id = account.id()
        self.manuscript = meta_manuscript.Manuscript()
        self.dt_now = datetime.datetime.now()

    #read tweets
    def classify(self):
        since = None
        classify_words = ["褒めて","ほめて","讃えて","たたえて","えらい","バオワ","ばおわ","バイト終","バおわ","実験終","らぼりだ","ラボ離脱","ラボりだ","帰宅"]
        ohayou_words = ["おはよう","起床","起きた"]
        transform_commands = ["変身"]
        test_command = ["_test_"]
        exclusion_words = ["bot","ビジネス","副業","公式"]

        public_tweets = self.api.home_timeline(count=50,since_id=since)

        count = {"ignore":0,
        "praise":0,
        "greeting":0}

        for tweet in public_tweets:
            user_name = tweet.user.name#HN
            screen_name = tweet.user.screen_name
            exclude = False

            for str in exclusion_words:
                if str in user_name:
                    exclude = True
                    # print("ignore that account")
                    count["ignore"] += 1
                    break
                else:
                    exclude = False

            if exclude == False:
                user_name_ = user_name.split("@")

                #返信part
                for classify_word in classify_words:
                    if classify_word in tweet.text:
                        if tweet.favorited == False:
                            print("test:承認")
                            count["praise"] += 1
                            #reply
                            self.reply(user_name_[0],screen_name,tweet.id,tweet.text)
                            #favorite
                            self.api.create_favorite(tweet.id)
                        else:
                            print("you already replyed it!")

                #挨拶part
                if 6 <= self.dt_now.hour <= 10:
                    for ohayou_word in ohayou_words:
                        if ohayou_word in tweet.text:
                            if tweet.favorited == False:
                                print("test:greeting")
                                count["greeting"] += 1
                                self.greeting(user_name_[0],screen_name,tweet.id,tweet.text)
                                self.api.create_favorite(tweet.id)
                            else:
                                print("you already replyed it!")

                #変身part
                for transform_command in transform_commands:
                    if transform_command in tweet.text:
                        if tweet.favorited == False:
                            print("test:　変身")
                            #transform
                            self.transform()
                            self.api.create_favorite(tweet.id)

                #test part
                if test_command[0] in tweet.text:
                    if tweet.favorited == False and screen_name == "yosyuaomenww":
                        self.test()
                        self.api.create_favorite(tweet.id)

        print("褒めた人数:{0}人\n無効な人数:{1}人\n挨拶した人数:{2}人".format(count["praise"],count["ignore"],count["greeting"]))

    #返事をする
    def reply(self,user_name,screen_name,tweet_id,tweet_text):
        num = random.randint(0,len(self.manuscript.tweet))
        # num_padded = '{0:03d}'.format(num) #ゼロパディング:0で３桁左詰する。 example 1→001
        reply = "@"+screen_name+"\n "+user_name+self.manuscript.tweet[num]
        self.api.update_status(status=reply, in_reply_to_status_id=tweet_id)#status
        print("{0}のツイート:{1} に{2}と応援しました!".format(user_name,tweet_text,reply))

    def greeting(self,user_name,screen_name,tweet_id,tweet_text):
        num = random.randint(0,len(self.manuscript.greeting))
        reply = "@"+screen_name+"\n "+user_name+self.manuscript.greeting[num]
        self.api.update_status(status=reply, in_reply_to_status_id=tweet_id)#status
        print("{0}のツイート:{1} に{2}と応援しました!".format(user_name,tweet_text,reply))

    #フォロバする
    def followback(self):
        #最近のフォロワーからその人のtweetやid情報取得
        # followers=api.followers_ids(screen_name=twitter_id)#全てのフォロワーidを取得
        # friends=api.friends_ids(twitter_id)#フォローしている人のidを取得
        followers = self.api.followers_ids(self.twitter_id)
        friends = self.api.friends_ids(self.twitter_id)

        follow_back = list(set(followers)-set(friends))#list フォロバすべき
        print("フォローバックした人数:{0}人".format(len(follow_back)))

        for i in range(min(len(follow_back),10)):
            try:
                self.api.create_friendship(follow_back[i])
                print("success follow!"+str(follow_back[i]))
            except tweepy.error.Tweeperror:
                print("error")

    def tweet(self):
        status = "順調だもん!"
        self.api.update_status(status=status)

    def transform(self):
        pass
        # status = "変身だもん"
        # self.api.update_status(status=status)

    def test(self):
        status = "起きてるモン！\n⊂・ー・つ"
        self.api.update_status(status=status)

def main():
    hometamon = Hometamon()
    hometamon.classify()
    hometamon.followback()

def lambda_handler(event, context):
    main()

if __name__ == "__main__":
    main()
