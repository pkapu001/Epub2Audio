from epubreader import EpubReader
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import pickle
from tqdm import tqdm
import os
from os import system as sys
from Apikeys import *
import subprocess


bookname = 'Slime_ln11'
flderpath = 'Slime_LN11'
book = EpubReader(bookname)
adpath = f"/sdcard/Audiobooks/{flderpath}/"
flderpath = 'Slime_LN11'



apikey ,url = paid_apikey, paid_url
# apikey ,url = free_apikey, free_url


authenticator = IAMAuthenticator(apikey)
tts = TextToSpeechV1(authenticator=authenticator)
tts.set_service_url(url)

OLDMAXSIZE = 5120 -300
MAXSIZE = 5120 -1000
BITRATE = 142.02

_NAME = 'name'
_CONTENT = 'content'


get_size = lambda t: len(t.encode('utf-8'))

get_time = lambda b: (len(b) / BITRATE) / 3600


def split_by_size(items, max_size, get_size=len):
    buffer = []
    buffer_size = 0
    for item in items:
        item_size = get_size(item)
        if buffer_size + item_size + len(buffer)+5 <= max_size:
            buffer.append(item)
            buffer_size += item_size
        else:
            buffer = ' '.join(buffer)
            yield buffer
            buffer = [item]
            buffer_size = item_size
    if buffer_size > 0:
        yield ' '.join(buffer)

for k, chapter in book.chapters.items():
    c_name = chapter[_NAME]
    text = chapter[_CONTENT]
    print(f'====={c_name} : Size: {len(text)}=====')
    splits = list(split_by_size(text.split(),MAXSIZE, get_size))


    for split in tqdm(splits):
        res = tts.synthesize(split, accept='audio/mp3', voice='en-US_AllisonV3Voice').get_result()
        if content == None:
            content = res.content
        else:
            content += res.content
        if get_time(content) >= 30:
            print(f'====={c_name}.{part} finished')
            f_name = f'{flderpath}/{str(k).zfill(2)}_{book.bookname}_{c_name}.{part}.mp3'
            with open(f_name, 'wb') as audio_file:
                audio_file.write(content)
            sys(f"adb push {f_name} {adpath}")

            content = None
            part += 1
    print(f'====={c_name}.{part} finished')
    f_name = f'{flderpath}/{str(k).zfill(2)}_{book.bookname}_{c_name}.{part}.mp3'
    with open(f_name, 'wb') as audio_file:
        audio_file.write(content)
    sys(f"adb push {f_name} {adpath}")
    content = None
    part = 1


''' send files to android phone through ADB'''
# files = [ f for f in os.listdir(flderpath) if f.endswith('.mp3')]
# for f in files:
#     f = f".\{flderpath}\{f}"
#     print(f)
#     sys(f"adb push {f} {adpath}")
# print('hello')