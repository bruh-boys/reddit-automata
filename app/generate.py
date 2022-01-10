
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
        img.putalpha(0)
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
            "libx264", "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k",
            "-shortest", "videos/"+n+"mp4"
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
I'm putting my extremely profoundly disabled 7 year old into a residential facility so I can forget he exists. I'm not sorry.I can't tell anyone this, even my therapist. Lambast me if you wanr and maybe I even deserve it. I only ask what you would do if you were in my situation. Not what you think "people should" do. What you would REALLY do. 

I'm a single mom of 2 boys. 12 and 7. My husband passed away 3 years ago in a work accident. A very large portion of me believe it was a suicide. I can't see him EVER making the mistake he made that caused his death, and he had taken an action just before that which ensured his co-workers weren't in the room. I fully believe he killed himself because of our younger son and no one will ever change my mind. 

We were told when I was pregnant that he would have Downs Syndrome. We could handle that. Even if it was severe. It turned out he has a chromosome deletion. His disorder is kind of rare so I won't post which specific one but suffice to say he'll never be anything more than he is now or has ever been. 

And what he is, is nothing. 

He doesn't appear to have any awareness and never has. His eyes are locked in one position, he doesn't respond to noise, touch, or pain. He is total care. He is capable of nothing. He is tube fed and on oxygen. He is in diapers and will be forever. He makes no sounds, no attempts to communicate. He never even really cried as a baby.

He has never made an attempt to interact with anyone or his environment. 

I'm not upset because I got a special needs/"imperfect" child. I feel the way I feel because this...... thing..... takes up 200% of my time and does NOTHING. I didn't get an imperfect child. I didn't get *a child*. 

I don't love him. He doesn't have any personality, there is nothing to love. And yet I'm responsible for him. In addition to his extreme delays he's also medically fragile. Respiratory crises, fecal impactions (his autonomic nervous system doesn't function properly), issues with his G tube, infections, pressure sores no matter WHAT we put him on or how we position him. 

Our older son has suffered because his non existent brother has colored everything in his life. He's had medical care get delayed because there's only one of me and hos brother is more critical. We do have a visiting home nurse but only 20 hrs/week and we aren't eligible for more. I was starting law school, I gave up my dreams and my plan for my children for this potato. My older son can't do a lot of things he wants to do because of the youngers need for care and appointments. 

The final straw was I heard a sound. I went into Younger Son's room to check, thinking he had forgotten how to breathe again, and saw Older Son hitting him and screaming "You're why I don't have a mother! You're why I don't have a father! You're why I can't have friends over! You're why I can't be in sports! I didn't ask for you and I hope you die!" 

Instead of being horrified, I watched. And Younger Son just did. not. react. No signs of pain or fear or upset. No reaction at all. 

He breathes but he is not alive. He doesn't know who I am. He doesn't know who Older Son is. He has no sense of self, life experience, or awareness of his surroundings. 

He doesn't need to be in my home. He doesn't know or care where he is. He is genetically my son but he is not family. My previously abused, brain damaged cat who can't walk straight has more personality and is far more loveable than my "child". In fact I was looking FORWARD to raising a Downs baby. Even one with severe impairments, for that reason. With disability can come gifts. This boy is not a gift. He is a genetic mistake I probably should have miscarried and would have definitely terminated if I'd known he would be like this. And the flip side is, if he HAS awareness..... he's miserable. And there is nothing I can do. If he has likes and dislikes no one knows what they are. If he is in pain he can't tell anyone. If he wants anything, he can't communicate. He's had every imaginable therapy, nothing has made a difference. 

And so he's leaving our home on the 29th. I feel excited and relieved and then guilty because I know we'll be happier with him gone. 

He's already taken my husband and my son's father. He was working so so so much OT to pay for the cucumber's care. For the experimental therapies insurance wouldn't cover. Because THIS one was going to be the BREAKTHROUGH. He was tired and defeated and disappointed. He sought counseling as well but I don't think he could ever say the words "I don't want my son in my home" either. 

He's ruined my older son. I was so wrapped up on the younger I never realized how ignored and damaged he was. He lost his father too. I didn't just lose my husband. HE is my priority now and this malignant lump can be someone else's problem. At least they'll be paid a wage to care for him. At least they'll get a break from him when they punch out. 

I just want to never think of him again and I'm not sorry. And for that, I'm sorry. 

Thanks for reading.

Edit: Thanks /u/piconeeks, for calling me a liar. Are you a medical doctor? If your Google Fu was any good you would have stumbled on 3p mosaic deletion-duplication syndrome. That is the disorder my son has. I've basically identified myself by posting that but hey, it's better than the PMs telling me to kill myself. If you look at the features of 3p deletion syndromes *they look like Downs*. My insurance didn't cover AFP testing which would have told us it WASN'T Downs and I didn't think we needed it. I had a regular ultrasound and a 3D. Both Drs were "99% sure it was Downs". 

This post was absolutely NOT fiction. Instead the mods and especially /u/piconeeks just "decided" it was. 

If anyone would like I'll doxx myself. You can see my ID to verify my name, my marriage license, and my husband's death certificate. I will then link you to the news article of the "freak industrial accident" that ended his life so you can see it's the same person. 

As for not choosing hospice for my son - I can't. About a year ago I myself was hospitalized with severe depression and C-PTSD (there is proof of that too). During that time my late husbands mother petitioned to get control as my son's medical proxy and got it. I'm fighting it but it's a long, complicated process. There are competency hearings. There are statements from doctors and evaluations. Unless SHE oks hospice, which she refuses, I cannot decide that. I have custody. I cannot ake medical decisions. She agreed to residential care which I feel is the second best option. So, he's going into residential care. 

As for "mistaking" a child choking with hitting, I was downstairs. I couldn't hear what my older son was saying. I only knew he was speaking. Go punch a blanket or, idk, a person with weak muscle tone. Then ask said person with weak muscle done to cough. They don't cough normally/forcefully. It's more a "strong puff". Similar to, again.... idk... a muted punch. When you're used to jumping at every strange sound, it's difficult to discern what's what sometimes. 

So, /u/piconeeks..... anything else you'd like to know? Care to admit I *just might be* telling the truth? There were identify details I left out but guess y'all need them.
"""
#generate_images(test,(5,10),"test",400,300,"font/arial-unicode-ms.ttf")
generate_audio(test,(5,10),"test",400,300,"en")
"""
clear_directory("videos")
clear_directory("audio")
clear_directory("images")
"""
