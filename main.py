import os, sys
MainFolderDir = os.getcwd()
sys.path.append(MainFolderDir + "\\Data\\PIP Packages")
import urllib.request
from bs4 import BeautifulSoup
import requests
from PIL import Image
import shutil
import pytesseract
from gtts import gTTS
import eyed3
from random import randint
import moviepy.editor as mp
from moviepy.editor import concatenate_videoclips
import moviepy.audio.fx.all as afx
from moviepy.editor import *



#Functions
def textRefine(text):
    n = 0
    while n < 3:
        if 'No.' in text:
            start = text.split('No.', 1)
            text = start[1]
            text = text[9:]
            text = ' ' + text
        elif 'NO.' in text:
            start = text.split('NO.', 1)
            text = start[1]
            text = text[9:]
            text = ' ' + text
        if 'View Thread' in text:
            end = text.split('View Thread')
            text = end[0]
            text = text[:-11]
        if 'JPG' in text:
            textnew = text.split('JPG', 1)
            text1 = textnew[0]
            text1 = text1[:-7]
            text1 = text1 + ' '
            text2 = textnew[1]
            text = str(text1 + text2)
        elif 'PNG' in text:
            textnew = text.split('PNG', 1)
            text1 = textnew[0]
            text1 = text1[:-7]
            text1 = text1 + ' '
            text2 = textnew[1]
            text = str(text1 + text2)
        elif 'png' in text:
            textnew = text.split('png', 1)
            text1 = textnew[0]
            text1 = text1[:-14]
            text1 = text1 + ' '
            text2 = textnew[1]
            text = str(text1 + text2)
        elif 'GIF' in text:
            textnew = text.split('GIF', 1)
            text1 = textnew[0]
            text1 = text1[:-7]
            text1 = text1 + ' '
            text2 = textnew[1]
            text = str(text1 + text2)
        symbols = '\/~()-*_."'
        for char in symbols:
            text = text.replace(char, ' ')
        n+=1
    text = text.replace('\n', ' ')
    text = text.replace('>', " \n")
    text = text.replace('|', "I")
    text = text.replace(' ur ', 'your')
    text = text.replace('stable', '')
    text = text.replace('mfw', 'my face when')
    text = text.replace(' fim ', ' ')
    text = text.replace('HS', 'high school')
    text = text.replace('7!', 'f')
    text = text.replace('j ', 'i ')
    text = text.replace('karoke', 'karaoke')
    return text

#Video Settings
full_vid_len = 341
video_speed = 1

checkforrepeats = 0

url = input("URL: ")
# EXAMPLE url = "https://www.reddit.com/r/wholesomegreentext/comments/1crdhuh/anon_goes_to_the_gym/#lightbox" <-- LIGHTBOX NOT NECESSARY

if checkforrepeats == 1:
    titles_file = open(MainFolderDir + "\\Data\\Videos Uploaded.txt", "r")
    titles = titles_file.read()
    if url in titles:
        print("Repeat!")
        quit()

if "#lightbox" not in url:
    url = url + "/#lightbox"

num = 1
while True:
    page = requests.get(url)
    data = page.text
    soup = BeautifulSoup(data, 'html.parser')
    images = soup.findAll('img')[num]
    source = images.get("src")
    if "i.redd.it" in source:
        imgurl = source
        break
    else:
        num += 1

lc = 0
sc = 0
for l in url:
    if l == '/':
        sc += 1
        if sc == 7:
            title = url[(lc+1):-10]
    lc += 1
title = title.replace('_', ' ')
title = title.replace('/', '')
title = title.capitalize()
print(title)

folderdir = MainFolderDir + "\\Videos\\" + title
os.mkdir(os.path.join(folderdir))
if ".jpeg" in imgurl: imgtype = ".jpeg"
elif ".png" in imgurl: imgtype = ".png"
elif ".webp" in imgurl: imgtype = ".webp"
else:
    print("ERROR: Not recognised URL")
    quit()

imagedir = folderdir + "\\textimage" + imgtype
urllib.request.urlretrieve(imgurl, imagedir)

basewidth = 1040
img = Image.open(imagedir)
img = img.convert("RGB")
wpercent = (basewidth / float(img.size[0]))
hsize = int((float(img.size[1]) * float(wpercent)))
img = img.resize((basewidth, hsize), Image.Resampling.LANCZOS)
img.save(os.path.join(folderdir + "\\" + "Img resized.jpg"))
os.remove(imagedir)

ImLength = img.size[1]
SplitNum = round(ImLength / (basewidth / 2))
totalSplitNum = SplitNum
print("Splits: " + str(SplitNum))

indent = 10

while SplitNum > 0:
    shutil.copy(folderdir + r"\\" + "Img resized.jpg", folderdir + r"\\" + str(SplitNum) +".jpg")
    im1 = Image.open(folderdir + r"\\" + str(SplitNum) +".jpg")
    width, height = im1.size
    left = 0
    right = width


    if totalSplitNum == 1:
        top = 0
        bottom = height
    elif totalSplitNum == 2:
        if SplitNum == 1:
            top = 0
            bottom = height / 2 + indent
        elif SplitNum == 2:
            top = height/2 - indent
            bottom = height
    elif totalSplitNum == 3:
        if SplitNum == 1:
            top = 0
            bottom = height /(totalSplitNum) + indent
        elif SplitNum == 3:
            top = 2*height /(totalSplitNum) - indent
            bottom = height
        elif SplitNum == 2:
            top = height /(totalSplitNum) - indent
            bottom = 2*height/(totalSplitNum) + indent
    elif totalSplitNum == 4:
        if SplitNum == 1:
            top = 0
            bottom = height / (totalSplitNum) + indent
        elif SplitNum == 4:
            top = (SplitNum-1)*height / (totalSplitNum) - indent
            bottom = height
        elif SplitNum == 2:
            top = (SplitNum-1)*height / (totalSplitNum) - indent
            bottom = (SplitNum)*height/(totalSplitNum) + indent
        elif SplitNum == 3:
            top = (SplitNum-1)*height / (totalSplitNum) - indent
            bottom = (SplitNum) * height / (totalSplitNum) + indent
    else:
        print("Image too long")
        quit()
    img2 = img.crop((left, top, right, bottom))
    img2.save(os.path.join(folderdir + "\\" + str(SplitNum) + str(SplitNum) +".jpg"))
    SplitNum -= 1

img.close()
PyTesseractDir = MainFolderDir + "\\Data\\Tesseract-OCR\\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = PyTesseractDir
img = Image.open(folderdir + "\\Img resized.jpg")
text = pytesseract.image_to_string(img)
refText = textRefine(text)

text_file = open(folderdir + "\\" +"CHECK TEXT.txt", "w")
text_file.write(refText)
text_file.close()
os.system("notepad.exe " + folderdir + "\\" +"CHECK TEXT.txt")

text_file = open(folderdir + "\\" +"CHECK TEXT.txt", "r")
text_file_contents = text_file.read()
language = 'en'
tld = 'ca'
myobj = gTTS(text=text_file_contents, lang=language, slow=False, tld=tld)
myobj.save(os.path.join(folderdir + "\\" + "TTS.mp3"))
text_file.close()

mp3_path = (folderdir + r"\\" + "TTS.mp3")
mp3_length = int(eyed3.load(folderdir + r"\\" + "TTS.mp3").info.time_secs)

first_img_ratio = 0.67
vidSplits = totalSplitNum
video_start = randint(0, (full_vid_len - mp3_length))
if 137 < video_start < 150: video_start = video_start + 13
video_end = video_start + mp3_length
img1_length = mp3_length * (first_img_ratio/(totalSplitNum-(1-first_img_ratio)))
notimg1_length = mp3_length * (1/(totalSplitNum-(1-first_img_ratio)))

fullvideo = mp.VideoFileClip(MainFolderDir + "\\Data\\fullvid.mp4")
fullvideo_mute = fullvideo.without_audio()
video = fullvideo_mute.subclip(video_start, video_end)

while vidSplits > 0:
    img = (mp.ImageClip(folderdir + "\\" + str(vidSplits) + str(vidSplits) + ".jpg"))
    if vidSplits == 1:
        img_length = img1_length
        starttime = 0
        endtime = img1_length
        video1 = video.subclip(starttime, endtime)
        video1 = video1.set_duration(img_length)
        img = img.set_duration(img_length)
        video1 = mp.CompositeVideoClip([video1, img.set_position("center")])
        vidSplits -=1
    elif vidSplits == 2:
        img_length = notimg1_length
        starttime = img1_length
        endtime = starttime + notimg1_length
        video2 = video.subclip(starttime, endtime)
        video2 = video2.set_duration(img_length)
        img = img.set_duration(img_length)
        video2 = mp.CompositeVideoClip([video2, img.set_position("center")])
        vidSplits -=1
    elif vidSplits == 3:
        img_length = notimg1_length
        starttime = img1_length + notimg1_length
        endtime = starttime + notimg1_length
        video3 = video.subclip(starttime, endtime)
        video3 = video3.set_duration(img_length)
        img = img.set_duration(img_length)
        video3 = mp.CompositeVideoClip([video3, img.set_position("center")])
        vidSplits -=1
    elif vidSplits == 4:
        img_length = notimg1_length
        sclip1 = 1
        eclip1 = 0
        starttime = sclip1*((img1_length) + (vidSplits - 1 - sclip1) * sclip1*img_length)
        endtime = (starttime + (eclip1*img1_length)) + (sclip1*img_length)
        video4 = video.subclip(starttime, endtime)
        video4 = video4.set_duration(img_length)
        img = img.set_duration(img_length)
        video4 = mp.CompositeVideoClip([video4, img.set_position("center")])
        vidSplits -=1

if totalSplitNum == 1: final_vid = concatenate_videoclips([video1])
elif totalSplitNum == 2: final_vid = concatenate_videoclips([video1,video2])
elif totalSplitNum == 3: final_vid = concatenate_videoclips([video1,video2,video3])
elif totalSplitNum == 4: final_vid = concatenate_videoclips([video1,video2,video3,video4])

TTS = AudioFileClip(folderdir + "\\TTS.mp3")
TTS = TTS.fx(afx.volumex, 0.7)
music = AudioFileClip(MainFolderDir + "\\Data\\music.mp3")

if 120 > mp3_length:
    music_clip = music.subclip(22, (mp3_length + 22 + 3))
else:
    print("Video too long!")
    quit()

followvid = mp.VideoFileClip(MainFolderDir + "\\Data\\followvid.mp4")
followvid = followvid.resize( (1080, 1920) )
music_clip = music_clip.fx(afx.volumex, 0.4)
audioclip = CompositeAudioClip([TTS, music_clip])
final_clip = concatenate_videoclips([final_vid, followvid])
final_clip = final_clip.set_audio(audioclip)
final_clip = final_clip.set_duration(mp3_length + 3)
print("duration = " + str(final_clip.duration + 3) + "s")
final_clip.write_videofile(MainFolderDir + "\\Videos\\" + title + ".mp4", temp_audiofile='temp-audio.m4a', remove_temp=True, codec="libx264", audio_codec="aac")

im1.close()
img2.close()
img.close()
shutil.rmtree(folderdir)

text_file = open(MainFolderDir + "\\Data\\Videos Uploaded.txt", "r+")
file_content = text_file.read()
text_file.seek(0)
text = title + " - " + url + "\n\n"
text_file.seek(0)
text_file.write(text + file_content)
file_content = text_file.read()
text_file.close()

print("\n\n\n" + title + " 🤖 #greentext#reddit#fyp#foryou#trending")