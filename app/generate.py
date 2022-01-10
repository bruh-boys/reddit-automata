
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


def generate_images(text: str, font_size: Tuple[int,int], name: str, width: int, height: int, font_path: str) -> None:
    clear_directory("images")
    
    (_, h) = font_size
    font = ImageFont.truetype(
        font_path, h)

    pages =divide_text(text, width-h*3, height-h*3, font_size)
    for i, page in enumerate(pages):
        img = Image.new('RGB', ( width,height), color=(0, 0, 0))
       
        ImageDraw.Draw(img).text((0,0), page, font=font, fill=(255, 255, 255))
        img.save("images/"+name+str(i)+".png")

# this is going to generate the audio for the videos


def generate_audio(text: str, font_size: Tuple[int,int], name: str,width:int, height: int, language) -> None:
    clear_directory("audio")
    (_, h) = font_size

    pages = divide_text(text, width-h*3, height-h*3, font_size)

    for i, page in enumerate(pages):
        gTTS(text=page.replace("\n"," "), lang=language).save("audio/"+name+str(i)+".mp3")


# this is going to generate the videos for then join them
def generate_videos(text: str, font_size: Tuple[int,int], name: str, width: int, height: int, font_path: str, language) -> None:
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


def concat_all(text: str, font_size: Tuple[int,int], name: str, width: int, height: int, font_path: str = "font/arial-unicode-ms.ttf", language="en") -> None:

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
October 30th, 2016, Results: Summer Of Code 2016.
This has been a long time coming but we wanted to give a proper closure to our participation in this run of the program and it takes time. Sometimes it's just to get the final report for each project trimmed down, others, is finalizing whatever was still in progress when the program finished: final patches need to be merged, TODO lists stabilized, future plans agreed; you name it.

Without further ado, here's the silver-lining for each one of the projects we sought to complete during this Summer of Code season:

FFv1 (Mentor: Michael Niedermayer)
Stanislav Dolganov designed and implemented experimental support for motion estimation and compensation in the lossless FFV1 codec. The design and implementation is based on the snow video codec, which uses OBMC. Stanislav's work proved that significant compression gains can be achieved with inter frame compression. FFmpeg welcomes Stanislav to continue working beyond this proof of concept and bring its advances into the official FFV1 specification within the IETF.

Self test coverage (Mentor: Michael Niedermayer)
Petru Rares Sincraian added several self-tests to FFmpeg and successfully went through the in-some-cases tedious process of fine tuning tests parameters to avoid known and hard to avoid problems, like checksum mismatches due to rounding errors on the myriad of platforms we support. His work has improved the code coverage of our self tests considerably.
"""
#generate_images(test,(5,10),"test",400,300,"font/arial-unicode-ms.ttf")
concat_all(test,(5,10),"test",400,300)
"""
clear_directory("videos")
clear_directory("audio")
clear_directory("images")
"""
