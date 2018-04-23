import requests
import re
import random
import configparser
from bs4 import BeautifulSoup

#PTT crawler
def ptt_hot():
    target_url = 'http://disp.cc/b/PttHot'
    #print('Start parsing pttHot....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    ptt_hot = ""
    counter = 0

    for data in soup.select('#list div.row2 div span.listTitle'):
        match = re.search(r'.*href="(.*?)"',str(data))
        if match:
            counter += 1
            title = data.text
            link = "http://disp.cc/b/" + match.group(1)
            ptt_hot += '{}\n{}\n\n'.format(title, link)
            if counter == 5:
                break

    return ptt_hot

#Youtube crawler
def youtube_hot():
    target_url = 'https://www.youtube.com.tw/feed/trending'
    #print('Start parsing youtube...')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text,'html.parser')
    youtube_hot = ""
    counter = 0

    for data in soup.select('h3'):
        match = re.search(r'.*href="(.*?)" title="(.*?)"',str(data))
        if match:
            counter += 1
            title = match.group(2)
            link = "https://www.youtube.com" + match.group(1)
            youtube_hot += '{}\n{}\n\n'.format(title, link)
            if counter == 5:
                break

    youtube_hot = youtube_hot[:len(youtube_hot)-1]
    return youtube_hot

#Dcard crawler
def dcard_hot():
    target_url = 'https://www.dcard.tw/f'
    #print('Start parsing dcard...')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text,'html.parser')
    dcard_hot = ""
    counter = 0

    for data in soup.select('a'):
        match = re.search(r'.*href="(/f/.*?/p/\d{9})-(.*?)"',str(data))
        if match:
            counter += 1
            title = match.group(2)
            link = "https://www.dcard.tw/" + match.group(1)
            dcard_hot += '{}\n{}\n\n'.format(title, link)
            if counter == 5: # number of article
                break

    dcard_hot = dcard_hot[:len(dcard_hot)-1]
    return dcard_hot
