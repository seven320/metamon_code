# encoding: utf-8

import unittest
from unittest.mock import Mock, patch
import copy
import pickle

import hometamon

# save api info

# api = copy.deepcopy(hometamon_class.api)
# api_return_value = api.home_timeline(count = 50)

# with open('./sample.pickle', mode='wb') as f:
#     pickle.dump(api_return_value, f)

hometamon_class = hometamon.Hometamon(test = True)
mock_api = Mock(name = "home_timeline")
with open('./sample.pickle', mode = 'rb') as f:
            pickel_data = pickle.load(f)

        mock_api.home_timeline.return_value = pickel_data
        self.hometamon_class.api = mock_api


class TestStringMethods(unittest.TestCase):
    def test_get_tweet(self):
        public_tweets = self.hometamon_class.api.home_timeline()
        cnt = 0
        
        for tweet in public_tweets:
            cnt += 1
        self.assertEqual(cnt == 50)


    def test_cnt(self):
        public_tweets = self.hometamon_class.api.home_timeline()
        count_reply = self.hometamon_class(public_tweets)
        print(count_reply)

        self.assertEqual(sum(count_reply.values()) == len(public_tweets))

    # def test_classify(self):
    #     load_tweets = "example.txt"
    #     hometamon_class = hometamon.Hometamon(test = True) 
    #     self.assertTrue(hometamon_class.classify(load_tweets))

    # def test_state(self):




    



if __name__ == "__main__":
    unittest.main()