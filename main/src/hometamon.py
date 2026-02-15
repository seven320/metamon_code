# encoding utf-8
import os, sys
import random
import datetime as dt
import unicodedata

from dotenv import load_dotenv

import tweepy

pardir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)

from src import meta_manuscript


class Hometamon:
    def __init__(self):
        if os.path.exists("/env/.env"):
            load_dotenv("/env/.env")
        elif os.path.exists("env/.env"):
            load_dotenv("env/.env")
        else:
            print("error doesn't exist .env path")

        if os.path.dirname("images"):
            self.image_dir = "images"
        elif os.path.dirname("/images"):
            self.image_dir = "/images"

        consumer_key = os.environ.get("CONSUMER_KEY") or ""
        consumer_secret = os.environ.get("CONSUMER_SECRET") or ""
        access_token = os.environ.get("ACCESS_TOKEN") or ""
        token_secret = os.environ.get("TOKEN_SECRET") or ""

        auth = tweepy.OAuthHandler(
            consumer_key=consumer_key, consumer_secret=consumer_secret
        )
        auth.set_access_token(key=access_token, secret=token_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)
        self.my_twitter_user_id = os.environ.get("TWITTER_USER_ID")
        self.manuscript = meta_manuscript.Manuscript()
        JST = dt.timezone(dt.timedelta(hours=+9), "JST")
        self.JST = dt.datetime.now(JST)
        self.admin_twitter_id = os.environ.get("ADMIN_RECIPIENT_ID")

        self.exclusion_user_names = [
            "bot",
            "ビジネス",
            "副業",
            "公式",
            "株",
            "FX",
            "ブランド",
            "無料",
            "キャリア",
            "エージェント",
            "LINE",
            "エロ",
            "オフパコ",
            "おふぱこ",
            "裏垢",
            "セフレ",
            "セックスレス",
        ]  # user name
        self.exclusion_words = ["peing", "http"]
        self.exclution_descriptions = [
            # 性的コンテンツ
            "アダルト",
            "エロ",
            "セクシャル",
            "18+",
            "グラビア",
            "美女",
            "美少女",
            "ヌード",
            "下着",
            "大人のおもちゃ",
            "風俗",
            "出会い系",
            "エッチ",
            "AV",
            "ポルノ",
            "裏垢",
            "パコ",
            "おふぱこ",
            "セフレ",
            "メンズエステ",
            "デリヘル",
            "スパム",
            "spam",
            "ボット",
            "bot",
            "ゲット",
            "無料",
            "キャンペーン",
            "アンケート",
            "企画",
            "LINE",
            "詐欺",
            "偽情報",
            "フェイクニュース",
            "fake news",
            "返金",
            "refund",
            "クレジットカード",
            "カード情報",
            "個人情報",
            "金儲け",
            "お金",
            "投資",
            "トレード",
            "FX",
            # 薬物や医療
            "医療",
            "薬",
            "ドクター",
            "doctor",
            "クリニック",
            "clinic",
            "ED",
            "育毛",
            "ダイエット",
            "美容",
            "整形",
            "美容外科",
            "健康",
            "ハーブ",
            "サプリメント",
            # ビジネス行為など
            "マルチ商法",
            "ネズミ講",
            "詐欺商法",
            "MLM",
            "ビジネスチャンス",
            "business opportunity",
            "副業",
            "在宅ワーク",
            "自由な生活",
            "自由な時間",
            "ノマドワーク",
            "稼ぐ",
            "儲ける",
            "年収",
            "月収",
            "資産",
            "利益",
        ]
        self.good_morning_words = ["おはよう", "ぽきた", "起きた", "起床", "早起き"]
        self.good_night_words = ["おやすみ", "寝よう", "寝る", "寝ます"]
        self.classify_words = [
            "褒めて",
            "ほめて",
            "バオワ",
            "ばおわ",
            "バイト終",
            "バおわ",
            "実験終",
            "実験おわ",
            "らぼりだ",
            "ラボ離脱",
            "ラボりだ",
            "ラボリダ",
            "帰宅",
            "疲れた",
            "つかれた",
            "ちゅかれた",
            "仕事納め",
            "仕事おわり",
            "退勤",
            "仕事終わり",
            "掃除終",
            "掃除した",
            "がこおわ",
            "学校終",
        ]
        self.set_task_words = ["設定"]
        self.transform_words = ["変身"]
        self.test_words = ["__test__"]
        self.counts = {
            "ignore": 0,
            "praise": 0,
            "good_morning": 0,
            "good_night": 0,
            "pass": 0,
            "transform": 0,
            "test": 0,
        }

    def get_tweets(self):
        return self.api.home_timeline(count=100, since_id=None)

    def user_name_changer(self, user_name):
        #  正規化
        normalize_user_name = unicodedata.normalize("NFKC", user_name)
        if "@" in normalize_user_name:
            normalize_user_name = normalize_user_name.split("@")[0]
        return normalize_user_name

    def good_morning(self, tweet):
        # image_ratio = 0.000001
        reply = (
            "@"
            + tweet.user.screen_name
            + "\n"
            + self.user_name_changer(tweet.user.name)
            + random.choice(self.manuscript.good_morning)
        )
        self.counts["good_morning"] += 1
        # if random.random() < image_ratio:
        #     pass
        # else:
        self.api.update_status(status=reply, in_reply_to_status_id=tweet.id)
        self.api.create_favorite(tweet.id)
        return reply

    def good_night(self, tweet, image_ratio=0.2):
        reply = (
            "@"
            + tweet.user.screen_name
            + "\n"
            + self.user_name_changer(tweet.user.name)
            + random.choice(self.manuscript.good_night)
        )
        self.counts["good_night"] += 1
        if random.random() < image_ratio:
            image_file = os.path.join(self.image_dir, "oyasumi_w_newtext.png")
            self.api.update_with_media(
                filename=image_file, status=reply, in_reply_to_status_id=tweet.id
            )
        else:
            self.api.update_status(status=reply, in_reply_to_status_id=tweet.id)
        self.api.create_favorite(tweet.id)
        return reply

    def choose_image_by_reply(self, reply: str) -> str:
        # replyの言葉から画像を選ぶ
        image_name = "erai_w_newtext.png"
        for otukare in ["お疲れ", "飲む", "休"]:  # 飲み物を運んでくれるようなリプライ
            if otukare in reply:
                image_name = "otukare_w_newtext.png"
        for yosi in ["よし", "えらい", "すごい"]:  # 頭撫でるイメージのリプライ
            if yosi in reply:
                image_name = "yosi_w_newtext.png"
        return image_name

    def praise(self, tweet, image_ratio=0.2):
        reply = (
            "@"
            + tweet.user.screen_name
            + "\n"
            + self.user_name_changer(tweet.user.name)
            + random.choice(self.manuscript.reply)
        )
        self.counts["praise"] += 1
        if random.random() < image_ratio:
            image_name = self.choose_image_by_reply(reply)
            image_file = os.path.join(self.image_dir, image_name)
            self.api.update_with_media(
                filename=image_file, status=reply, in_reply_to_status_id=tweet.id
            )
        else:
            self.api.update_status(status=reply, in_reply_to_status_id=tweet.id)
        self.api.create_favorite(tweet.id)
        return reply

    def tweet_sweet(self):
        status = random.choice(self.manuscript.sweet_tweet_before)
        status += (
            "\n⊂・ー・つ" + chr(int(random.choice(self.manuscript.sweets), 16)) + "\n"
        )  # 16進数から変換
        status += random.choice(self.manuscript.sweet_tweet_after)
        self.api.update_status(status=status)

    def test_tweet_linestamp(self):
        reply = "ぼくのLINEスタンプがでたもん!!!ぼくのかわりにみんなをほめてほしいもん!!よろしくもん!!\nhttps://store.line.me/stickershop/product/17652748"
        image_file = os.path.join(self.image_dir, "stamp", "all.png")
        self.api.update_with_media(filename=image_file, status=reply)

    def test_tweet(self, image_flg=False):
        status = "起きてるもん！\n⊂・ー・つ"
        if image_flg:
            image_file = os.path.join(self.image_dir, "icon.jpg")
            self.api.update_with_media(filename=image_file, status=status)
        else:
            self.api.update_status(status=status)
        self.counts["test"] += 1
        return status

    def check_exclude(self, tweet):  # 除外するかどうかcheck
        if str(tweet.user.id) == self.my_twitter_user_id:
            return True
        elif tweet.favorited:
            return True
        elif tweet.text.split(" ")[0] == "RT":
            return True
        elif tweet.text.split(" ")[0][0] == "@":
            if "@denden_by" in tweet.text:
                # hometaskの設定が入っていれば無視．
                if self.set_task_words[0] in tweet.text:
                    return True
                else:  # 自分に向けてのtweetかつ，設定が入っていないならファボ
                    self.api.create_favorite(id=tweet.id)
            return True
        elif (
            len(tweet.text) >= 80
        ):  # if tweet is more than 80 words, it will be ignored
            return True
        for exclusion_word in self.exclusion_words:
            if exclusion_word in tweet.text:
                return True
        if self.exclude_user(tweet.user):  # 特定のユーザー情報を含む場合除外
            return True
        return False

    def check_good_morning(self, tweet):  # 返事するかどうかcheck
        if 5 <= self.JST.hour <= 9:
            for good_morning_word in self.good_morning_words:
                if good_morning_word in tweet.text:
                    return True
        return False

    def check_good_night(self, tweet):
        if 22 <= self.JST.hour or self.JST.hour <= 1:
            for good_night_word in self.good_night_words:
                if good_night_word in tweet.text:
                    return True
        return False

    # NOTE: 毎日15時にお菓子を進めるツイートをする
    def check_sweet(self):
        return self.JST.hour == 15 and 0 <= self.JST.minute <= 5

    # NOTE: 一ヶ月に一回宣伝ツイートを実行する
    def check_tweet_linestamp(self):
        return (
            self.JST.day == 12 and self.JST.hour == 18 and 15 <= self.JST.minute <= 20
        )

    def check_reply(self, tweet):
        for classify_word in self.classify_words:
            if classify_word in tweet.text:
                return True
        return False

    def check_transform(self, tweet):
        for transform_word in self.transform_words:
            if transform_word in tweet.text:
                return True
        return False

    def check_test(self, tweet):
        for test_word in self.test_words:
            if tweet.user.screen_name == "yosyuaomenww" and test_word in tweet.text:
                return True
        return False

    def check_image_flg(self, tweet):
        return tweet.user.screen_name == "yosyuaomenww" and "image" in tweet.text

    def classify(self, tweet):
        reply = ""
        if self.check_exclude(tweet):
            self.counts["ignore"] += 1
        else:
            if self.check_good_morning(tweet):
                reply = self.good_morning(tweet)
            elif self.check_good_night(tweet):
                reply = self.good_night(tweet)
            elif self.check_reply(tweet):
                reply = self.praise(tweet)
            elif self.check_transform(tweet):
                reply = self.transform()
            elif self.check_test(tweet):
                reply = self.test_tweet(image_flg=self.check_image_flg(tweet))
            else:
                self.counts["pass"] += 1
        return reply

    def transform(self):
        self.counts["transform"] += 1
        return ""

    def exclude_user(self, user_status):
        # ユーザー名に特定の単語が入っている場合
        for exclusion_name in self.exclusion_user_names:
            if exclusion_name in user_status.name:
                return True
        if user_status.description is None:
            return False
        # ユーザーの目的欄に特定の単語が入っている場合
        for exclusion_description in self.exclution_descriptions:
            if exclusion_description in user_status.description:
                return True
        return False

    def follower_management(self):
        # フォローしているユーザーのリストを取得する処理
        followers = self.api.followers_ids(self.my_twitter_user_id)
        friends = self.api.friends_ids(self.my_twitter_user_id)
        follow_back = list(set(followers) - set(friends))

        random.shuffle(follow_back)
        user_statuses = self.api.lookup_users(follow_back[:100])
        cnt = 0
        for user_status in user_statuses:
            # フォローしている中で適切でないユーザー名や自己紹介欄をしているユーザーをアンフォローする処理
            if self.exclude_user(user_status):
                # self.api.destroy_friendship(id=user_status.id)
                # cnt += 1
                pass
            elif not user_status.follow_request_sent:
                try:
                    self.api.create_friendship(id=user_status.id)
                    cnt += 1
                except tweepy.error.TweepError as e:
                    print(e)
                    cnt += 1
            if cnt > 10:
                break

    def report(self):
        result = "time:{}\n褒めた数:{}\n除外した数:{}\n挨拶した数:{}\n反応しなかった数:{}\n変身:{}\nテスト数:{}\n合計:{}だもん！".format(
            self.JST.strftime("%Y/%m/%d %H:%M:%S"),
            self.counts["praise"],
            self.counts["ignore"],
            self.counts["good_morning"] + self.counts["good_night"],
            self.counts["pass"],
            self.counts["transform"],
            self.counts["test"],
            sum(self.counts.values()),
        )
        self.api.send_direct_message(self.admin_twitter_id, result)
        print(result)
        return result


def main():
    hometamon = Hometamon()
    public_tweets = hometamon.get_tweets()
    for public_tweet in public_tweets:
        hometamon.classify(public_tweet)
    if hometamon.check_sweet():
        hometamon.tweet_sweet()
    if hometamon.check_tweet_linestamp():
        hometamon.tweet_linestamp()
    hometamon.follower_management()
    hometamon.report()


if __name__ == "__main__":
    main()
