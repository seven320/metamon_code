#encoding:utf-8

# 参考にしたmecab dictionary[https://github.com/neologd/mecab-ipadic-neologd/blob/master/README.ja.md]



import MeCab

m = MeCab.Tagger()
mt = MeCab.Tagger("-Ochasen -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/")

print(m.parse("すもももももももものうち"))

print(mt.parseToNode("すもももももももものうち"))
