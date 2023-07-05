import requests
from misskey import Misskey
import json


if os.path.exists("/env/.env"):
    load_dotenv("/env/.env")
elif os.path.exists("env/.env"):
    load_dotenv("env/.env")
else:
    print("error doesn't exist .env path")

api_key = os.environ.get("API")

mk = Misskey("social.camph.net", i = api_key)  # Input instance address (If leaved no attribute, it sets "misskey.io")

# Let's note!
# mk.notes_create(
#     text="Hello Misskey.py!"
# )


# read local TL(おそらく入っているサーバーのタイムライン)
# notes = mk.notes_local_timeline(100)
notes = mk.notes_timeline(with_files =False)
# notes = mk.notes_global_timeline(100)
# print(notes)
# print(dir(mk))
print(len(notes))
for n in notes:
    print(f'{n["user"]["name"]}, {n["text"]}')
    # if n["user"] == "電電":
    #     print(n)
    #     break








