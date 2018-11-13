#encoding utf-8

import tweepy

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

    #read tweets
    def classify(self):
        since = None
        classify_list = ["褒めて","ほめて","讃えて","たたえて","えらい"]
        transform_command = ["変身"]
        exclusion_list = ["bot","ビジネス","副業","公式"]

        public_tweets = self.api.home_timeline(count=50,since_id=since)

        for tweet in public_tweets:
            user_name = tweet.user.name#HN
            screen_name = tweet.user.screen_name

            for i in range(len(exclusion)):
                if exclusion_list[i] in user_name:
                    print("not reply")
                else:
                    user_name = user_name.split("@")
                    for i in range(len(classify_list)):
                        if classify_list[i] in tweet.text:
                            if tweet.favorited == False:
                                print("test:承認")
                                #reply
                                self.reply(user_name[0],screen_name,tweet.id,tweet.text)
                                #favorite
                                self.api.create_favorite(tweet.id)
                            else:
                                print("you already replyed it!")

                    for i in range(len(transform_command)):
                        if transform_command[i] in tweet.text:
                            if tweet.favorited == False:
                                print("test:　変身")
                                #transform
                                self.transform()
                                self.api.create_favorite(tweet.id)

    #返事をする
    def reply(self,user_name,screen_name,tweet_id,tweet_text):
        num = random.randint(1,tweet.max_num())
        num_padded = '{0:03d}'.format(num) #ゼロパディング:0で３桁左詰する。 example 1→001

        reply = "@"+screen_name+"\n "+user_name+tweet.manus(num-1)
        self.api.update_status(status=reply, in_reply_to_status_id=tweet_id)#status
        print("{0}のツイート:{1} に{2}と応援しました!".format(user_name,tweet_text,reply))

    #フォロバする
    def followback(self):
        #最近のフォロワーからその人のtweetやid情報取得
        # followers=api.followers_ids(screen_name=twitter_id)#全てのフォロワーidを取得
        # friends=api.friends_ids(twitter_id)#フォローしている人のidを取得
        followers = self.api.followers_ids(self.twitter_id)
        friends = self.api.friends_ids(twitter_id)

        follow_back = list(set(followers)-set(friends))#list フォロバすべき
        print("list_followback,count:",len(follow_back))

        for i in range(min(len(followback),10)):
            try:
                self.api.create_friendship(followback[i])
                print("success follow!"+str(followback[i]))
            except tweepy.error.Tweeperror:
                print("error")

    def tweet(self):
        status = "順調だもん!"
        self.api.update_status(status=status)

    def transform(self):
        pass

def main():
    hometamon = Hometamon()
    hometamon.classify()
    hometamon.followback()

if __name__ == "__main__":
    # print("aa")
    main()
