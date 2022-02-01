
from PIL import Image, ImageDraw, ImageFont

from typing import Tuple

from .text import divide_text
from gtts import gTTS
from os import listdir, remove
from subprocess import call
from time import sleep


def clear_directory(directory: str) -> None:
    for file in listdir(directory):
        remove(directory+"/"+file)
# this is going to generate the images for then use it for the videos


def generate_images(text: str, font_size: int, name: str, width: int, height: int, font_path: str) -> None:
    clear_directory("images")

    font = ImageFont.truetype(
        font_path, font_size)

    pages = divide_text(text, width-font_size*2, height-font_size*2, font_size)
    for i, page in enumerate(pages):
        img = Image.new('RGB', (width, height), color=(0, 0, 0))

        ImageDraw.Draw(img).text((font_size, font_size),
                                 page, font=font, fill=(255, 255, 255))
        img.save("images/"+name+str(i)+".png")


def generate_audio(text: str, font_size: int, name: str, width: int, height: int, language) -> None:
    clear_directory("audio")

    pages = divide_text(text, width-font_size*2, height-font_size*2, font_size)

    for i, page in enumerate(pages):
        gTTS(text=page.replace("\n", " "), lang=language).save(
            "audio/"+name+str(i)+".mp3")


# this is going to generate the videos for then join them
def generate_videos(text: str, font_size: int, name: str, width: int, height: int, font_path: str, language) -> None:
    clear_directory("videos")

    generate_images(text, font_size, name, width, height, font_path=font_path)
    generate_audio(text, font_size, name, width, height, language=language)

    names = [name+str(i)+"." for i in range(len(listdir("images")))]

    for n in names:
        call([
            "ffmpeg", "-loop", "1", "-i", "images/" +
            n+"png", "-i", "audio/"+n+"mp3", "-c:v",
            "libx264", "-c:a", "aac", "-shortest", "videos/"+n+"mp4"
        ])
    clear_directory("audio")
    clear_directory("images")


def concat_all(text: str, font_size: int, name: str, width: int, height: int, font_path: str = "font/arial-unicode-ms.ttf", language="en") -> None:
    generate_videos(text, font_size, name, width, height,
                    font_path=font_path, language=language)

    video_paths = ["file 'videos/"+name +
                   str(i)+".mp4'\n" for i in range(len(listdir("videos")))]

    with open("video_list.txt", "w") as f:
        f.writelines(video_paths)
    call(["ffmpeg", "-safe", "0", "-f", "concat", "-i", "video_list.txt",
         "-c", "copy", "video/"+name+".mp4"])
    clear_directory("videos")
