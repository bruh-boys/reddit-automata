
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

text="""
Okay, I pull up, hop out at the after party
You and all your friends, yeah, they love to get naughty
Sippin' on that Henn', I know you love that Bacardi (Sonny Digital)
1942, I take you back in that 'Rari
Okay, I pull up, hop out at the after party
You and all your friends, yeah, they love to get naughty
Sippin' on that Henn', I know you love that Bacardi
1942, I take you back in that 'Rari
Switchin' lanes and I'm seein' lights, you know I watch the curb
Smokin' weed, you know I'm gettin' high, you know it calm my nerves
Trappin' hard, pumpin' non-stop, the bag I had to earn
You can try, but you might fail again, you know you never learn
Came in with a bottle, I was trippin'
And I took a couple shots and now I'm dizzy
It got me burning up, burning up
Insides burning up, burning up (Yeah)
Okay, I pull up, hop out at the after party
You and all your friends, yeah, they love to get naughty
Sippin' on that Henn', I know you love that Bacardi
1942, I take you back in that 'Rari
Okay, I pull up, hop out at the after party
You and all your friends, yeah, they love to get naughty
Sippin' on that Henn', I know you love that Bacardi
1942, I take you back in that 'Rari
Uh, poppin' meds (Uh), out in the meadows (Yeah)
She like a little red (Uh), in her stilettos (Yeah)
Anytime you live (Uh), out in the ghetto (Yeah)
You try to duck the feds (Uh), they need to let go
Came in with a bottle, I was trippin'
And I took a couple shots, it got me dizzy
It got me burning up, burning up
Insides burning up, burning up (Yeah)
Okay, I pull up, hop out at the after party
You and all your friends, yeah, they love to get naughty
Sippin' on that Henn', I know you love that Bacardi
1942, I take you back in that 'Rari
Okay, I pull up, hop out at the after party
You and all your friends, yeah, they love to get naughty
Sippin' on that Henn', I know you love that Bacardi
1942, I take you back in that 'Rari
Okay, I pull up (Okay, I pull up)
Okay, I pull up (Okay, I pull up)
Okay, I pull up (Okay, I pull up), hop out at the after party
Okay, I pull up (Okay, I pull up), hop out at the after party
Okay, I pull up (Okay, I pull up), hop out at the after party
Okay, I pull up (Okay, I pull up), hop out at the after party
"""

concat_all(text,10,"okayIPullUp",400,400)
