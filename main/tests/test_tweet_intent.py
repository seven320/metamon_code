import urllib.parse

from src import tweet_intent 

def test_make_intent_url():
    text = "早く寝る"
    intent_url = tweet_intent.make(text)
    parameters = intent_url.split("?")[-1]
    dic = urllib.parse.parse_qs(parameters)
    assert dic['text'][0] == text

def test_make_intent_url_with_hashtag():
    text = "task を設定"
    hashtag = "hometask"
    intent_url = tweet_intent.make(text, hashtag = hashtag)
    parameters = intent_url.split("?")[-1]
    dic = urllib.parse.parse_qs(parameters)
    assert dic['text'][0] == text
    assert dic["hashtags"][0] == hashtag

def test_make_intent_url_with_tweet_to():
    text = "task を設定"
    tweet_to = "denden_by"
    intent_url = tweet_intent.make(text, tweet_to= tweet_to)
    parameters = intent_url.split("?")[-1]
    dic = urllib.parse.parse_qs(parameters)
    assert dic['text'][0] == "@{} ".format(tweet_to) + text