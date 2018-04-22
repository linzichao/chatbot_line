from flask import Flask, request, abort
from linebot import (
        LineBotApi, WebhookHandler
)
from linebot.exceptions import (
        InvalidSignatureError
)
from linebot.models import *

import os
import requests
import re
import random
import configparser
from bs4 import BeautifulSoup

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(os.environ.get('ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.environ.get('SECRET'))

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

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
            if counter == 10:
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
            if counter == 10:
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
            if counter == 10: # number of article
                break

    dcard_hot = dcard_hot[:len(dcard_hot)-1]
    return dcard_hot


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    #print(event.source.user_id)

    if event.message.text == "PTT熱門文章":
        content = ptt_hot()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
        return 0

    if event.message.text == "Youtube熱門影片":
        content = youtube_hot()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
        return 0

    if event.message.text == "Dcard熱門文章":
        content = dcard_hot()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
        return 0

    '''
    if event.message.text == "Debug":
        message = TextSendMessage(text="Debug: " + event.message.text)
        line_bot_api.reply_message(event.reply_token, message)
        message2 = TextSendMessage(text="Debug2: " + event.message.text)
        line_bot_api.push_message(event.source.user_id, message2)
        return 0
    '''

    if event.message.text == "了解資超":
        buttons_template = TemplateSendMessage(
            alt_text='個人資料 目錄',
            template=ButtonsTemplate(
                title='了解作者(林資超)',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/2UaRtwH.jpg',
                actions=[
                    MessageTemplateAction(
                        label='個性',
                        text='個性'
                    ),
                    MessageTemplateAction(
                        label='專長',
                        text='專長'
                    ),
                    MessageTemplateAction(
                        label='系上活動參與',
                        text='系上活動參與'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0

    if event.message.text == "更多功能":
        buttons_template = TemplateSendMessage(
            alt_text='更多功能 目錄',
            template=ButtonsTemplate(
                title='Chatbot額外功能',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/lgPvzHB.png',
                actions=[
                    MessageTemplateAction(
                        label='PTT熱門文章',
                        text='PTT熱門文章'
                    ),
                    MessageTemplateAction(
                        label='Dcard熱門文章',
                        text='Dcard熱門文章'
                    ),
                    MessageTemplateAction(
                        label='Youtube熱門影片',
                        text='Youtube熱門影片'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
