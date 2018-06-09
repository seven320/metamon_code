#encoding:utf-8
import sys
import MeCab
import tweepy

#親ディレクトリにあるアカウント情報へのパス
import sys,os
pardir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)

#account情報をaccount.pyからロード
from account import account #load account

text="月が綺麗ですね。メロンパン。メロン。パン"

# nm=MeCab
def NLP(text):#natural language processing
    m = MeCab.Tagger("-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")
    # print(m.parse(text))
    return m.parse(text)

def sprit_text_to_noun(text,frequency_dic):
    m = MeCab.Tagger("-Ochasen -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")
    #自然言語処理
    node=m.parse(text)

    pos=node.split("\n")#単語ごとに切ってリストに格納
    for i in range(len(pos)):
        if "名詞" in pos[i]:#名詞だけ抽出
            print(pos[i])
            noun=pos[i].split("\t")[0]
            if noun in frequency_dic.keys():
                frequency_dic[noun]+=1
            else:
                frequency_dic.update({noun:1})
    print(frequency_dic)

def main():
    auth=account.Initialize()
    api = tweepy.API(auth)
    twitter_id=account.id()

    public_tweets = api.home_timeline(count=100)

    frequency_dic={}
    for tweet in public_tweets:
        print("\n"+tweet.user.name)
        # print(tweet.user.screen_name)#@以下のID
        print(tweet.text)
        print(sprit_text_to_noun(tweet.text,frequency_dic))

if __name__=="__main__":
    # sprit_text_to_noun(text)
    main()
