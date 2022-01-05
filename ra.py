#!/bin/python3
import requests
from dotenv import load_dotenv
import os
from gtts import gTTS
import shutil
import argparse
from time import sleep
from video import video


def main():
    load_dotenv()
    os.system("mkdir -p data")  # create the folder if doesent exists
    auth = requests.auth.HTTPBasicAuth(os.getenv("ID"), os.getenv("SECRET"))

    data = {
        'grant_type': 'password',
        'username': os.getenv("REDDIT_USERNAME"),
        'password': os.getenv("PASSWORD")
    }

    headers = {'User-Agent': 'test/0.0.1'}  # the name of the bot/app

    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth,
                        data=data,
                        headers=headers)

    TOKEN = res.json()['access_token']

    headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

    # while the token is valid (~2 hours) we just add headers=headers to our requests
    requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

    # ./ra.py -s subreddit -l language
    parser = argparse.ArgumentParser(
        description=
        'Get subreddit posts, and save them in varius formats(mp3, txt, mp4)')

    parser.add_argument('-s',
                        '--subreddit',
                        help='subreddit to get posts from',
                        type=str,
                        required=True)

    parser.add_argument('-l',
                        '--language',
                        help='language to save the posts in',
                        type=str,
                        required=True)
    args = parser.parse_args()
    res = requests.get(f"https://oauth.reddit.com/r/{args.subreddit}",
                       headers=headers)

    for post in res.json()["data"]["children"]:
        x = post['data']['title']
        print(f"Title: {x}")
        print(f"""upvotes:{post['data']['ups']}""")
        body = post['data']['selftext']
        if body == "":
            print("No body")
            body = "No body"
            history = x
        else:
            print(f"Body length: {len(body)}")
            body = post['data']['selftext']
            history = x + " " + body
        url_img = post['data']['url']
        if not url_img.endswith(".jpg"):
            print("No image")
            url_img = "https://media.discordapp.net/attachments/744419261086433282/928387662283427930/tyler.jpg"
        else:
            url_img = post['data']['url']
            print(f"url: {url_img}")
        res = requests.get(url_img, headers=headers)
        img = requests.get(url_img,
                           stream=True)  # download the image from the url
        with open(f'data/{x.replace("/"," ")}.jpg', 'wb') as out_file:
            shutil.copyfileobj(img.raw, out_file)
        del img
        f = open(f'data/{x.replace("/"," ")}.txt', "w")
        f.write(history)
        f.close
        t = gTTS(text=history, lang=args.language)
        if body != "":
            t.save(f'data/{x.replace("/"," ")}.mp3')
        else:
            print("no text")
        # if the image doesen't end with .jpg or .png, we replace it with tyler.jpg
        video(f'data/{x.replace("/"," ")}.jpg',
              f'data/{x.replace("/"," ")}.mp3',
              f'data/{x.replace("/"," ")}.mp4')
        sleep(5)
        print("---------------------------------------------------")
        #sleep(3600)


if __name__ == '__main__':
    main()
