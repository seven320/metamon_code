#encoding:utf-8

import os 
from os.path import join, dirname
from dotenv import load_dotenv


load_dotenv(".env")
API = os.environ.get("API_KEY")
print(API)
