# encoding utf-8
"""プラットフォーム非依存の判定ロジックとNGワード群。

X版 (hometamon.py) と mixi2版 (hometamon_mixi2.py) の両方から使う。
褒め文の選択や返信の送信といった副作用はここには置かず、純粋関数のみを置く。
"""

import unicodedata

# ユーザー名に含まれていたら除外する語
EXCLUSION_USER_NAMES = [
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
]

# 本文に含まれていたら除外する語
EXCLUSION_WORDS = ["peing", "http"]

# プロフィール(自己紹介)に含まれていたら除外する語
EXCLUSION_DESCRIPTIONS = [
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

# 本文に含まれていたら「褒める」トリガーとなる語
PRAISE_WORDS = [
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


def normalize_user_name(user_name):
    """表示名を正規化し、@以降を落とす。"""
    normalized = unicodedata.normalize("NFKC", user_name)
    if "@" in normalized:
        normalized = normalized.split("@")[0]
    return normalized


def is_excluded_user(name, description):
    """ユーザー名・プロフィールにNG語が含まれるか。"""
    for word in EXCLUSION_USER_NAMES:
        if word in name:
            return True
    if not description:
        return False
    for word in EXCLUSION_DESCRIPTIONS:
        if word in description:
            return True
    return False


def build_praise_reply(screen_name, display_name, phrase):
    """褒め返信文を組み立てる（@ハンドル + 改行 + 正規化した表示名 + 褒め文）。"""
    return "@" + screen_name + "\n" + normalize_user_name(display_name) + phrase


def has_excluded_word(text):
    """本文にNG語が含まれるか。"""
    return any(word in text for word in EXCLUSION_WORDS)


def is_praise_trigger(text):
    """本文が褒めトリガー語を含むか。"""
    return any(word in text for word in PRAISE_WORDS)


def choose_image_by_reply(reply):
    """返信文から添付画像を選ぶ。"""
    image_name = "erai_w_newtext.png"
    for otukare in ["お疲れ", "飲む", "休"]:  # 飲み物を運んでくれるようなリプライ
        if otukare in reply:
            image_name = "otukare_w_newtext.png"
    for yosi in ["よし", "えらい", "すごい"]:  # 頭撫でるイメージのリプライ
        if yosi in reply:
            image_name = "yosi_w_newtext.png"
    return image_name
