from urllib.request import urlopen, urlretrieve, Request
from bs4 import BeautifulSoup
import json
import os
import requests

def get_google_doodles_img_y(year):
    for i in range(1, 13):
        get_google_doodles_img_m(year, i)

def get_google_doodles_img_m(year, month):
    print('YEAR: {}, MONTH:{}'.format(year, month))
    url = 'https://www.google.com/doodles/json/' + str(year) + '/' + str(month) + '?hl=zh_TW'
    resp = urlopen(url)
    print(resp)

    doodles = json.load(resp, )

    dir_name = os.path.join('.','doodles', str(year), str(month))
    print(dir_name)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    for d in doodles:
        url = 'https:' + d['url']
        title = d['title']
        print('Url: ', url)
        print('Title: ', title)
        fpath = os.path.join(dir_name, os.path.basename(url))
        print(fpath)
        urlretrieve(url, fpath)

def get_tabelog_lst():
    url = 'https://tabelog.com/tw/tokyo/rstLst/?SrtT=rt'
    resp = urlopen(url)
    html = BeautifulSoup(resp)
    print(html)

def get_google_trans_audio(draft):
    src = None
    with open(draft, 'r', encoding='utf-8') as fp:
        src = fp.read()

    import nltk
    nltk.download('punkt')
    from nltk import tokenize
    tok_text = tokenize.sent_tokenize(src)
    all_content = b""

    for sentence in tok_text:
        print(sentence)

        url = 'https://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q='
        url = url + sentence

        resp = requests.get(url)
        resp.raise_for_status()
        audio = resp.content
        all_content = all_content + audio

    dir_name = 'audio'
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    f_name = os.path.join(dir_name, '1.mp3')
    with open(f_name, 'wb') as fp:
        fp.write(all_content)
    

    

    
