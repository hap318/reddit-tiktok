import os

import main
import praw
from moviepy.editor import concatenate_audioclips, AudioFileClip


reddit = praw.Reddit(
    client_id="1IN4RVKjDjkxPwEHL6XJLg",
    client_secret="tO5UgY60LMpS7pYC_R9_WxybL-lElA",
    user_agent="web:myredditapp:v1 (by u/epo_o)",
)


def cutText(text, seg):
    textCuts = []
    while len(text) > 250:
        cut = seg
        while text[cut] != " ":
            cut += 1
        cutOne = text[:cut]
        textCuts.append(cutOne)
        text = text[cut:]
    textCuts.append(text)
    return textCuts


def writeMp3s(myText):
    i = 1
    for s in cutText(myText, 250):
        fileName = str(i) + ".mp3"
        main.tts("en_us_010", s, fileName)
        i += 1
    print("Audio saved")
    return i-1


def concatenate_audio_moviepy(audio_clip_paths, output_path):
    """Concatenates several audio files into one audio file using MoviePy
    and save it to `output_path`. Note that extension (mp3, etc.) must be added to `output_path`"""
    clips = [AudioFileClip(c) for c in audio_clip_paths]
    final_clip = concatenate_audioclips(clips)
    final_clip.write_audiofile(output_path)


def mergeMp3s(num, name):
    files = []
    for i in range(num):
        fileName = str(i+1) + ".mp3"
        files.append(fileName)
    name = name.replace(" ", "")
    name = list(name)
    for letter in name:
        if not letter.isalpha():
            name.remove(letter)
    name = "".join(name)
    print(name)
    concatenate_audio_moviepy(files, name + ".mp3")
    for file in files:
        os.remove(file)


def getSubmissions():
    submissions = []
    for i, submission in enumerate(reddit.subreddit("AmItheAsshole").hot(limit=10)):
        print(i, submission.title)
        print(submission.url)
        submissions.append(submission)
    while True:
        ans = input("Pick post: ")
        ans = int(ans)
        print(submissions[ans].url)
        myText = submissions[ans].title + "...." + submissions[ans].selftext + "...."
        print(myText)
        num = writeMp3s(myText)
        mergeMp3s(num, submissions[ans].title)

def addTest():
    pass


getSubmissions()





