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
from metamon_code import meta_manuscript

class Hometamon():
    def __init__(self,test = True):
        auth = account.Initialize()
        self.api = tweepy.API(auth, wait_on_rate_limit=True)
        self.twitter_id = account.id()
        self.manuscript = meta_manuscript.Manuscript()
        JST = datetime.timezone(datetime.timedelta(hours=+9),"JST")
        self.jst_now = datetime.datetime.now(JST)
        #for test
        self.test = test

    #read tweets
    def classify(self):
        since = None
        classify_words = ["褒めて","ほめて","讃えて","えらい","バオワ","ばおわ","バイト終","バおわ","実験終","実験おわ","実験完全終了","らぼりだ","ラボ離脱","ラボりだ","帰宅","疲れた","つかれた","仕事納め","掃除終","掃除した"]
        ohayou_words = ["おはよう","起床","起きた"]
        oyasumi_words = ["おやすみ","寝よう","寝る"]
        transform_commands = ["変身"]
        test_command = ["_test_"]
        exclusion_words = ["bot","ビジネス","副業","公式","株"]

        public_tweets = self.api.home_timeline(count=50,since_id=since)

        count = {"ignore":0,
        "praise":0,
        "greeting_morning":0,
        "greeting_nignt":0,
        "pass":0}

        if self.test == True:
            print("#"*10,"test","#"*10)
        else:
            print("#"*10,"product","#"*10)

        tweet_count = 0
        for tweet in public_tweets:
            user_name = tweet.user.name#HN
            screen_name = tweet.user.screen_name#ID
            exclude = False
            tweet_count += 1

            tweet_split = tweet.text.split(" ")


            print(tweet_count,": ",end="")
            if self.test:
                print("text:",tweet.text)
            print("status:",end="")

            #自分には返事しない
            if screen_name == self.twitter_id:
                exclude = True
                print("this tweet is mine")

            #ファボしたツイートには反応しない
            elif tweet.favorited == True:
                exclude = True
                print("you alredy favorited")

            #RTには返事しない
            elif tweet_split[0] == "RT":
                exclude = True
                print("this is retweeted")

            elif tweet_split[0][0] == "@":
                exclude = True
                print("this is to someone")

            if exclude == False:
                #上記の除外ワードを含む人には返事しない
                for str in exclusion_words:
                    if str in user_name:
                        exclude = True
                        # print("ignore that account")
                        count["ignore"] += 1
                        print("this is ignored")
                        break

            if exclude == False:
                print("this is pass")
                user_name_ = user_name.split("@")
                #返信part
                for classify_word in classify_words:
                    if classify_word in tweet.text:
                        count["praise"] += 1
                        #reply
                        self.reply(user_name_[0],screen_name,tweet.id,tweet.text)
                        #favorite
                        self.api.create_favorite(tweet.id)
                        exclude = True
                        break

            if exclude == False:
                #挨拶part
                if 0 <= self.jst_now.hour <= 24:
                    for ohayou_word in ohayou_words:
                        if ohayou_word in tweet.text:
                            # print("-----test:greeting_morning")
                            count["greeting_morning"] += 1
                            self.greeting_morning(user_name_[0],screen_name,tweet.id,tweet.text)
                            self.api.create_favorite(tweet.id)
                            exclude = True
                            break

                if 22 <= self.jst_now.hour or self.jst_now.hour <= 2:
                    for oyasumi_word in oyasumi_words:
                        if oyasumi_word in tweet.text:
                            # print("-----test:good night")
                            count["greeting_nignt"] += 1
                            self.greeting_nignt(user_name_[0],screen_name,tweet.id,tweet.text)
                            self.api.create_favorite(tweet.id)
                            exclude = True
                            break

            if exclude == False:
                #変身part
                for transform_command in transform_commands:
                    if transform_command in tweet.text:
                        #transform
                        self.transform()
                        self.api.create_favorite(tweet.id)


                #test part
                if test_command[0] in tweet.text:
                    if screen_name == "yosyuaomenww":
                        self.test_tweet()
                        self.api.create_favorite(tweet.id)

        print("褒めた人数:{0}人\n無効な人数:{1}人\n挨拶した人数:{2}人".format(count["praise"],count["ignore"],count["greeting_morning"]))

    #返事をする
    def reply(self,user_name,screen_name,tweet_id,tweet_text):
        num = random.randint(0,len(self.manuscript.reply)-1)
        # num_padded = '{0:03d}'.format(num) #ゼロパディング:0で３桁左詰する。 example 1→001
        print(num)
        reply = "@"+screen_name+"\n "+user_name+self.manuscript.reply[num]
        if self.test == False:
            self.api.update_status(status=reply, in_reply_to_status_id=tweet_id)#status
        else:
            print("-----test:reply-----")
        print("tweet:{0}:{1} \nreply:{2}".format(user_name,tweet_text,reply))

    def greeting_morning(self,user_name,screen_name,tweet_id,tweet_text):
        num = random.randint(0,len(self.manuscript.greeting_morning)-1)
        reply = "@"+screen_name+"\n "+user_name+self.manuscript.greeting_morning[num]
        if self.test == False:
            self.api.update_status(status=reply, in_reply_to_status_id=tweet_id)#status
        else:
            print("-----test:greeting_morning-----")
        print("tweet:{0}:{1} \nreply:{2}".format(user_name,tweet_text,reply))

    def greeting_nignt(self,user_name,screen_name,tweet_id,tweet_text):
        num = random.randint(0,len(self.manuscript.greeting_night)-1)
        reply = "@"+screen_name+"\n "+user_name+self.manuscript.greeting_night[num]
        if self.test == False:
            self.api.update_status(status=reply, in_reply_to_status_id=tweet_id)
        else:
            print("-----test:greeting_night-----")
        print("tweet:{0}:{1} \nreply:{2}".format(user_name,tweet_text,reply))

    #フォロバする
    def followback(self):
        if self.test == True:
            print("-----test:followback-----")
        else:
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


    def test_tweet(self):
        if self.test == False:
            status = "起きてるもん！\n⊂・ー・つ"
        else:
            status = "ｚｚｚ"
        self.api.update_status(status=status)
        print(status,"とツイートしました．")


    def check_timeline(self):
        since = None
        public_tweets = self.api.home_timeline(count=10,since_id=since)
        print(self.twitter_id)

        for tweet in public_tweets:
            print("-"*20)
            # print(tweet)
            print(tweet.text)
            #RTには返事しない
            tweet_split = tweet.text.split(" ")
            if tweet_split[0] == "RT":
                exclude = True
                print("this is retweeted")
            elif tweet_split[0][0] == "@":
                exclude = True
                print("this is to someone")
            else:
                print("this is original")

            if tweet.user.screen_name == self.twitter_id:
                print("-"*10)
                print(tweet.user.name,tweet.user.screen_name,"\n",tweet.text)
            # print(tweet.user.name,tweet.user.screen_name)

def main(test):
    #test command
    hometamon = Hometamon(test)
    hometamon.classify()
    hometamon.followback()


def lambda_handler(event, context):
    main(test = False)
    # hometamon = Hometamon()
    # hometamon.check_timeline()


if __name__ == "__main__":
    main(test=True)
    # hometamon = Hometamon()
    # hometamon.check_timeline()
