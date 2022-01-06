import subprocess


def video(image_file: str, mp3_file: str, video_file: str) -> None:
    # audio.mp3 + image.jpg = video.mp4
    if image_file == "":
        print("no image")
    else:
        subprocess.call([
            "ffmpeg", "-loop", "1", "-i", image_file, "-i", mp3_file, "-c:v",
            "libx264", "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k",
            "-shortest", video_file
        ])
        return None
