#encoding:utf-8
class Manuscript():
    def __init__(self):
        self.tweet=[]
        #1~
        self.tweet.append("仕事終わらせてえらい！！")
        self.tweet.append("よく頑張りました！！！")
        self.tweet.append("満点！")
        self.tweet.append("いつも最高です。")
        self.tweet.append("とても優秀！")
        self.tweet.append("よっ、社長！！")
        self.tweet.append("できる人は違うね")
        self.tweet.append("頑張り屋さんです")
        self.tweet.append("えらい！\nとてもえらい！！")
        self.tweet.append("すばらしい！")
        self.tweet.append("最高！！仕事人！！！")

    def manus(self,num=0):
        return self.tweet[num]

    def max_num(self):
        return len(self.tweet)