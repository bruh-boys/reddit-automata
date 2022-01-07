import subprocess
import requests
from PIL import Image
import PIL

# audio.mp3 + image.jpg = video.mp4 and if the img is not divisible by 2, it will be resized


def convert_video(image_file: str, mp3_file: str, video_file: str) -> None:
    img_resolution = Image.open(image_file).size
    image = Image.open(image_file)
    print("resolution image: ", img_resolution)
    if img_resolution[0] % 2 != 0 or img_resolution[1] % 2 != 0 or img_resolution[0] > 1920 or img_resolution[1] > 1080:
        resized_image = image.resize((1920, 1080), PIL.Image.ANTIALIAS)
        resized_image.save(image_file)
        print("resized image: ", resized_image.size)
    subprocess.call([
        "ffmpeg", "-loop", "1", "-i", image_file, "-i", mp3_file, "-c:v",
        "libx264", "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k",
        "-shortest", video_file
    ])
    return None

# in this function we will be downloading the image from the url


def download_file(url: str, file_name: str) -> None:
    with open(file_name, "wb") as file:
        response = requests.get(url)
        file.write(response.content)
    del response
    return None
