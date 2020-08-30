# encoding:utf-8

import random
"""
返事ルール

カタカナは使わないこと
できるだけ広い意味で取られるような返事を書くこと
一人称は「僕」にすること
"""

class Manuscript:
    def __init__(self):
        self.tweet = [
        ]
        self.reply = [
            "仕事終わらせてすごいもん！！",
            # "つかれたもん〜",
            "よく頑張ったもん！！！",
            "満点だもん！！",
            "いつも最高です。",
            "とても優秀だもん！",
            "できる人は違うもん",
            "頑張り屋さんだもん",
            "すごい！\nとてもすごい！！",
            "すばらしいもん！",
            "最高！！仕事人！！！",
            # "行動力の化身！！！！",
            "今日も頑張ってるもん",
            "今日の成果も素晴らしいもん！！",
            "わんだふる！！！",
            "素晴らしい成果だもん！！",
            "素晴らしい出来栄えだもん",
            "仕事を頑張る姿が素敵だもん!!",
            "大好きだもん",
            "今日もお疲れ様だもん",
            "ゆっくり休むんだもん！！",
            "休憩も大事だもん",
            "君はひとりじゃないもん",
            "時には休息も必要だもん",
            "おつかれさまだもん",
            "すごいんだもん",
            "は偉いんだもん",
            "今日は大変だったもんね",
            "体を休めるもん\nつお布団",
            "今日は早く寝るもん",
            "よく頑張ったもん。\n僕も頑張るもん",
            "\nつ おふとん\nよく寝るんだもん!!",
            "風邪に気をつけるんだもん！！",
            "ゆっくり休むんだもん〜",
            "お疲れ様だもん",
            "大好きだもんよ〜",
            "\n今日はつかれたもんね",
            "ゆっくりお風呂にはいるんだもん",
            "えらいもん！！",
            "がんばっててえらい！",
            "お疲れ様だもん",
            "ゆっくり休むもん",
            "\nいつも一緒にいるもん",
            "お菓子食べてゆっくり休むもん",
            "休憩大事もんよ",
            "体よく休めるもん",
            "は今日も頑張ったもん！！",
            "ご飯よく食べて休憩するもん",
            "甘いものでも食べてゆっくり休むもん",
            "よく頑張ったもんよ",
            "よしよしもん\nヾ⊂・ー・つなでなで",
            "ゆっくりするもん",
            "お疲れ様だもん\nヾ⊂・ー・つ応援してるもん",
            "応援してるもん",
            "いつもこっそり応援してるもん⊂・ー・）",
            "休憩しっかりとるもん！！",
            "偉いもん",
            "いつも頑張ってるのみてるもんよ！",
            "好きだもんよ",
            "頑張ってるもん",
            "はえらいんだもん！！",
            "ゆっくり休むもん",
            "ちょっと休憩するもん",
            "大変だけど頑張ってて偉い！！",
            "見守ってるもんよ，いつも頑張ってるもん",
            "ちょっと休むもん",
            "大好きだもんよ〜\nゆっくりするもん！！",
            "よしよしだもん！！",
            "今日はあったかいもの飲むもん!!",
            "ちょっと休むんだもん"
        ]

        self.greeting_morning = [
            "おはようだもん！！",
            "起きて偉いんだもん",
            "おはよう。。。\nまだ眠いんだもん",
            "元気に頑張るもん",
            "今日もがんばるもん",
            "起きてえらいもん",
            "布団から出てえらい！！",
            "おはようもん！！",
            "\nおはようもん\n僕ももうちょっとで起きる。もん。。。"
            "起きてえらいもん",
            "おはようもん",
            "おはようもん\n今日もみんなを褒めてまわるもん",
            "おはようだもん\n僕ももうちょっとで布団から出るもん。。。",
            "おはようだもん\nもう5分だけ寝たいもん。",
            "おはようもん！！",
            "おはようだもん",
            "ぐっどもーにんぐだもん",
            "今日も負けずに頑張るもん！",
            "朝だもんね〜",
            "\nまだ眠いんだもん",
            "頑張ろうもん！！",
            "おきて偉いもん",
            "おはようだもん",
            "ぐっどもーにんぐだもん",
            "今日もがんばるもん！！",
            "えらいんだもん",
            "\nおはようだもん⊂・ー・つ",
            "朝起きれて偉いんだもん!!"
        ]

        self.greeting_night = [
            "お休みだもん!",
            "おやすみだもん！！",
            "おやすみだもん〜",
            "おやすみもん！",
            "よく寝るんだもん!",
            "いいゆめみるんだもん!",
            "おやすみなさいだもん",
            "疲れたもんね",
            "よしよしもん",
            "今日もお疲れ様だもん",
            "明日も頑張るもん",
            "おやすみだもんｚｚｚ",
            "ゆっくり寝るもん",
            "おやすみもん！！",
            "ゆっくり寝るもん",
            "おやすみなさいもん",
            "おやすみだもん",
            "ぐっどないとだもん！！",
            # "zzz",
            "よくねるもんよ",
            "早く寝るもん！！",
            "おやすみもんね\n今日は僕もすこ〜し疲れたもん",
            "ゆっくりねむるんだもん",
            "おやすみだもん\n良い夢みれるように祈ってるんだもん！！",
            "体冷やさないようにねるもん",
            "ちゃんと歯磨きしたもんか？おやすみだもん！！",
            "今日も頑張ったもん！！\nおやすみもん"
        ]

        self.sweet_tweet_before = [
            "お菓子の時間だもんよ〜",
            "3時だもんね〜\nお疲れ様だもん",
            "頑張ってるもん",
            "3時だもん\n休憩するもんよ〜",
            "おやつの時間だもん",
            "3時だもんよ〜",
            "ちょっと一息入れるもん",
            "休憩するもん〜",
            "みんなお疲れ様だもん",
            "3時だもんね\nうがい，手洗いしっかりしてゆっくりたべるもん",
            "おやつ食べるもん"
        ]

        self.sweet_tweet_after = [
            "ゆっくりするもん",
            "食べてちょっとゆっくりするもん",
            "もう一息だもん",
            "頑張ってるもんよ",
            "休憩も大事もんよ",
            "もう少しだもん",
            "がんばるもんよ〜"
        ]
 
 #  ref [https://lets-emoji.com/food-emoji/]
        self.sweets = [
            "U+1F950", # croissant
            "U+1F95E", #pancakes
            "U+1F9C7", # waffle
            "U+1F361", # dango
            "U+1F366", # soft ice cream
            "U+1F368", # ice cream
            "U+1F369", # doughnut
            "U+1F36A", # cookie
            "U+1F370", #shortcake
            "U+1F36B", # chocolate bar
            "U+1F36E", # custard
            "U+1F36C" # candy
        ]

        self.hometask_random_reply = [
            "よく頑張ったもん！！！",
            "とても優秀だもんよ！",
            "頑張り屋さんだもん",
            "今日も頑張ってるもんよ",
            "わんだふるだもん！！！",
            "仕事を頑張る姿が素敵だもん!!",
            "今日もお疲れ様だもんよ",
            "おつかれさまだもんよ！",
            "は今日も頑張って偉いんだもん",
            "お疲れ様だもん",
            "大好きだもんよ〜",
            "えらいもん！！",
            "よく頑張ったもんよ",
            "よしよしもん\nヾ⊂・ー・つなでなで",
            "大好きだもんよ〜\nゆっくりするもん！！",
            "よしよしだもん！！",
            "今日はあったかいもの飲むもん!!",
            "ちょっと休むんだもん"
        ]

        self.count_reply = {
            1:"最初の達成だもんね．偉いもん！！称号あげるもん\nつ",
            5:"5回目だもん，すごいもん!!これあげるもん!!!\nつ",
            10:"10回目だもん!!お疲れ様だもん!!この調子で続けるもん!!!\nつ",
            30:"30回目だもん!!この調子で頑張るもん!!!\nつ"
        }

        self.streak_reply = {
            3:"連続3日達成だもん!!!すごいもん!!これあげるもん\n銅メダルあげるもん!\nつ🥉",
            7:"連続7日hometask達成だもん!!!この調子で続けるもん!!\n銀メダルあげるもん\nつ🥈",
            14:"連続14日hometask達成だもん!!偉いもん!!\nこの調子で続けるもん\n金メダルあげるもん\nつ🥇"
        }
        
        # self.rewards = [
        #     "U+1F435", # monkey
        #     "U+1F98D", # gorilla
        #     "U+1F436", # dog
        #     "U+1F98A", # fox 
        #     "U+1F99D", # raccoon
        #     "U+1F431", # cat
        #     "U+1F434", # horse
        #     "U+1F993", # zebra
        #     "U+1F98C", # deer
        #     "U+1F404", # cow
        #     "U+1F417" # boar
        # ]

        self.icon = {
            1:"U+1F95A", # egg
            5:"U+1F423", # hatching chick
            10:"U+1F413", # rooster
            30:"U+1F985", # eagle
        }
