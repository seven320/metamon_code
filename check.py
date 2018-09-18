#encoding:utf-8
import tweepy

#親ディレクトリにあるアカウント情報へのパス
import sys,os
pardir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pardir)

from metamon_code import reply
#account情報をaccount.pyからロード
from account import account #load account
auth=account.Initialize()
api = tweepy.API(auth)


def main():
    states = api.rate_limit_status()
    print(states.keys())
    # print(states["rate_limit_context"])
    # print(states["resources"])
    print(states["resources"].keys())
    print(states["resources"]["tweets"])
    # resources_list = states[resources].keys()
    # print(resources_list)
    # for resource in resources_list:
    #     print(resource,":"states["resources"][resource])



if __name__ == "__main__":
    main()
