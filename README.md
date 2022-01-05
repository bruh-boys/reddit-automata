a simple script for automate getting data from reddit 

<h1>Features</h1>

- Download the stories, and save them to txt gile, and convert them to a mp3 file using gTTS

**In a Nutshell🥜**
```rs
bla_bla_bla.txt -> gTTS = bla_bla_bla.mp3 + bla_bla_bla.jpg -> ffmpeg -> bla_bla_bla.mp4
```

<h1>Want to use it?</h1>

Clone the repository.

Create a .env file with the following data.

You need to have installed ffmpeg,python3, and pip3.

```
PASSWORD=
REDDIT_USERNAME=
SECRET=
ID=
```

install the dependencies

```bash
$ pip3 install -r requirements.txt
```

<h1>Examples</h1>

```bash
$ ./ra.py -s "discordapp/hot" -l en
```

<img src="https://media.discordapp.net/attachments/786759600245309460/928214984771657788/unknown.png?width=631&height=432">


<img src="https://media.discordapp.net/attachments/786759600245309460/928217146654334976/unknown.png?width=223&height=432">

<h1>Example output:</h1>

https://user-images.githubusercontent.com/69026987/148291522-2bf5550d-6bdf-4057-8dba-f179547dff5b.mp4

<h1>TODO</h1>

- [ ] get the data without auth?

- [ ] manage errors




