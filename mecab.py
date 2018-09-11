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

def sprit_text_to_noun(text):
    frequency_dic = {}
    frequency_verb = {}
    m = MeCab.Tagger("-Ochasen -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")
    #自然言語処理
    node = m.parse(text)

    pos = node.split("\n")#単語ごとに切ってリストに格納
    for i in range(len(pos)):
        if "名詞" in pos[i]:#名詞だけ抽出
            # print(pos[i])
            noun = pos[i].split("\t")[0]
            if noun in frequency_dic.keys():
                frequency_dic[noun]+=1
            else:
                frequency_dic.update({noun:1})

        if "動詞" in pos[i]:#動詞だけ抽出
            print(pos[i])
            verb = pos[i].split("\t")[0]
            if verb in frequency_verb.keys():
                frequency_verb[verb]+=1
            else:
                frequency_verb.update({verb:1})
    print("名詞一覧：",frequency_dic)
    print("動詞一覧：",frequency_verb)

def main():
    auth = account.Initialize()
    api = tweepy.API(auth)
    twitter_id=account.id()

    public_tweets = api.home_timeline(count=100)

    for tweet in public_tweets:
        print("\n"+tweet.user.name)
        # print(tweet.user.screen_name)#@以下のID
        print(tweet.text)
        print(sprit_text_to_noun(tweet.text))

if __name__=="__main__":
    # sprit_text_to_noun(text)
    main()
