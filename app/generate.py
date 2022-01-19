
from PIL import Image, ImageDraw, ImageFont
from divide_text.text import divide_text
from typing import Tuple

from divide_text.text import divide_text
from gtts import gTTS
from os import listdir, remove
from subprocess import call


def clear_directory(directory: str) -> None:
    for file in listdir(directory):
        remove(directory+"/"+file)
# this is going to generate the images for then use it for the videos


def generate_images(text: str, font_size: int, name: str, width: int, height: int, font_path: str) -> None:
    clear_directory("images")
    
    
    font = ImageFont.truetype(
        font_path, font_size)

    pages =divide_text(text, width-font_size*2, height-font_size*2,font_size)
    for i, page in enumerate(pages):
        img = Image.new('RGB', ( width,height), color=(0, 0, 0))
       
        ImageDraw.Draw(img).text((font_size,font_size), page, font=font, fill=(255, 255, 255))
        img.save("images/"+name+str(i)+".png")

# this is going to generate the audio for the videos


def generate_audio(text: str, font_size: int, name: str,width:int, height: int, language) -> None:
    clear_directory("audio")
  

    pages = divide_text(text, width-font_size*2, height-font_size*2, font_size)
  

    for i, page in enumerate(pages):
        gTTS(text=page.replace("\n"," "), lang=language).save("audio/"+name+str(i)+".mp3")


# this is going to generate the videos for then join them
def generate_videos(text: str, font_size:int, name: str, width: int, height: int, font_path: str, language) -> None:
    clear_directory("videos")

    generate_images(text, font_size, name, width, height, font_path=font_path)
    generate_audio(text, font_size, name,width, height, language=language)

    names = [name+str(i)+"." for i in range(len(listdir("images")))]

    for n in names:
        call([
            "ffmpeg", "-loop", "1", "-i", "images/" +
            n+"png", "-i", "audio/"+n+"mp3", "-c:v",
            "libx264", "-c:a", "aac","-shortest", "videos/"+n+"mp4"
        ])
    clear_directory("audio")
    clear_directory("images")


def concat_all(text: str, font_size: int, name: str, width: int, height: int, font_path: str = "font/arial-unicode-ms.ttf", language="en") -> None:
    clear_directory("video")
    generate_videos(text, font_size, name, width, height,
                    font_path=font_path, language=language)

    video_paths = ["file 'videos/"+name +
                   str(i)+".mp4'\n" for i in range(len(listdir("videos")))]

    with open("video_list.txt", "w") as f:
        f.writelines(video_paths)
    call(["ffmpeg", "-f", "concat", "-i", "video_list.txt",
         "-c", "copy", "video/"+name+".mp4"])
    clear_directory("videos")


test = """
Doin your mom doin doin your mom Doin your mom doin doin your mom Doin doin your mom doin doin your mom You know we straight with doin your mom Doin your mom doin doin your mom Doin your mom doin doin your mom Doin doin your mom doin doin your mom You know we straight with doin your mom I'm doin your mom. 
Yes yours! I first saw her in the Wal-Mart pickin out your drawers. 
Big Dolly Parton hair like an 80s prom queen But her ass was lookin good all up in those mom-jeans. 
I approached her in the checkout line, and said yo baby wassup? She had two gallons of milk, and I was starin at her jugs. 
Five minutes later she agreed to get with me So we went and rocked the minivan like Giggity. 
Giggity. 
Giggity. 
I was ridin your mom like she was Mario Kart. 
I gave her a lift back to her crib cause her car wouldn't start. 
She invited me in the house, and we started makin out again. 
How many times I tap that ass? OVER 9000! Yeah. 
She called me Pledge cause I knocked the dust off it. 
She later made me a sandwich and she cut the crust off it. 
Cause she knows how I like it, and that I'm a little young To be in the bed, butt-naked doin your mom. 
Doin your mom doin doin your mom Doin your mom doin doin your mom Doin doin your mom doin doin your mom You know we straight with doin your mom Doin your mom doin doin your mom Doin your mom doin doin your mom Doin doin your mom doin doin your mom You know we straight with doin your mom I like your mamas big butt, and I cannot lie. 
You other brothers can't deny that she's fly. 
We make sexy time, yes and every night I tap that. 
She saw me butt-naked, now she thinks I'm half black. 
But your moms the best, the super M.I.L.F. 
Cause she loves to toss the salad even though she ain't a chef And I blame it on the al-al-al-cohol But If I were you, I wouldn't kiss your mom on the mouth at all. 
She likes the Donkey-Punch. 
She likes the Dirty Sanchez. 
Sometimes she even likes to fool around in your bed. 
She likes rough sex with handcuffs and I'll be honest She likes me to Chris Brown her when she acts like Rihanna. 
She's so therapeutic. 
When I need to cure my restlessness I br-br-br-br-br-br-br-br motorboat your moms breastestess. 
I didn't wanna tell you, but I had to write this song Cause I'm in your house every night doin your mo-om. 
Doin your mom doin doin your mom Doin your mom doin doin your mom Doin doin your mom doin doin your mom You know we straight with doin your mom Doin your mom doin doin your mom Doin your mom doin doin your mom Doin doin your mom doin doin your mom You know we straight with doin your mom I'm havin sex with your mother That makes me better than you. 
I'm havin sex with your mother That makes me better than you. 
Doin your mom doin doin your mom Doin your mom doin doin your mom Doin doin your mom doin doin your mom You know we straight with doin your mom Doin your mom doin doin your mom Doin your mom doin doin your mom Doin doin your mom doin doin your mom You know we straight with doin your mom 
 """
#print(divide_text(test, 500, 500, 20))
generate_images(test, 20, "test", 800, 600, font_path="font/arial-unicode-ms.ttf")
#concat_all(test, 10, "test", 400,300)
"""
clear_directory("videos")
clear_directory("audio")
clear_directory("images")
"""
