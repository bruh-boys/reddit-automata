#!/bin/python3
import requests
from dotenv import load_dotenv
import os
from gtts import gTTS
import shutil
import argparse
from time import sleep
from video import convert_video, download_file


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
        description='Get subreddit posts, and save them in varius formats(mp3, txt, mp4)')

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
        allow_format = ["jpg", "png", "gif", "jpeg"]
        if not url_img.endswith(tuple(allow_format)):
            print("allow formats:", tuple(allow_format))
            print("url_img:", url_img)
            print("No image,using tyler")
            url_img = "https://media.discordapp.net/attachments/744419261086433282/928387662283427930/tyler.jpg"
        else:
            url_img = post['data']['url']
            print(f"url: {url_img}")

        res = requests.get(url_img, headers=headers)
        img = requests.get(url_img,
                           stream=True)  # download the image from the url
        file = f'data/{x.replace("/"," ")}.{url_img.split(".")[-1]}'

        download_file(url_img, file)

        f = open(f'data/{x.replace("/"," ")}.txt', "w")

        f.write(history)

        f.close

        t = gTTS(text=history, lang=args.language)

        if body != "":
            t.save(f'data/{x.replace("/"," ")}.mp3')
        else:
            print("no text")
        convert_video(file,
                      f'data/{x.replace("/"," ")}.mp3',
                      f'data/{x.replace("/"," ")}.mp4')
        print("---------------------------------------------------------")

        for i in range(3):
            sleep(1)
            print(f"new video in:{i+1}")


if __name__ == '__main__':
    main()
