import gtts
import requests
from dotenv import load_dotenv
import os
from gtts import gTTS
from datetime import datetime

load_dotenv()
os.system("mkdir -p audios") # create the folder if doesent exists
auth = requests.auth.HTTPBasicAuth(os.getenv("ID"), os.getenv("SECRET"))

data = {'grant_type': 'password',
        'username': os.getenv("REDDIT_USERNAME"),
        'password': os.getenv("PASSWORD")}


headers = {'User-Agent': 'test/0.0.1'}


res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

TOKEN = res.json()['access_token']

headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

# while the token is valid (~2 hours) we just add headers=headers to our requests
requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

res = requests.get("https://oauth.reddit.com/r/AskReddit/hot",
                   headers=headers)
for post in res.json()["data"]["children"]:
    x = post['data']['title']
    print(x)
    print(f"""upvotes:{post['data']['ups']}""")
    print("---------------------------------------------------")
    f = open(f'audios/{x.replace("/"," ")}.txt',"w")
    f.write(x)
    f.close
    t = gTTS(text=x,lang="en")
    t.save(f'audios/{x.replace("/"," ")}.mp3') # the "/" is take as a space, so i replace it

