# encoding: utf-8
import urllib.parse

def make(text, tweet_to = "", url = "", hashtag = "", via = "", related = "", in_reply_to = ""):
    base_url = "https://twitter.com/intent/tweet"

    if not tweet_to == "":
        text = "@{} ".format(tweet_to) + text

    query_dic = {
        "text": text,
        "url": url,
        "hashtags": hashtag,
        "via": via,
        "in_reply_to": in_reply_to
    }

    parameters = urllib.parse.urlencode(query_dic)

    if len(parameters) > 0:
        web_intent_url = base_url + "?" + parameters
    else:
        web_intent_url = base_url

    return web_intent_url

if __name__ == "__main__":
    intent_url = make()
    print(intent_url)

    