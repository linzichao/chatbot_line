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


def ptt_hot():
    target_url = 'http://disp.cc/b/PttHot'
    print('Start parsing pttHot....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for data in soup.select('#list div.row2 div span.listTitle'):
        title = data.text
        link = "http://disp.cc/b/" + data.find('a')['href']
        if data.find('a')['href'] == "796-59l9":
            break
        content += '{}\n{}\n\n'.format(title, link)
    return content


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    print(event.source)
    print(type(event.source))

    ev = event.source
    print(ev)
    print(type(ev))

    if event.message.text == "熱門文章":
        content = ptt_hot()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
        return 0

    if event.message.text == "Debug":
        message = TextSendMessage(text="Debug: " + event.message.text)
        line_bot_api.reply_message(event.reply_token, message)
        message2 = TextSendMessage(text="Debug2: " + event.message.text)
        line_bot_api.push_message(ev.userId, message2)
        return 0


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
                        label='興趣',
                        text='興趣'
                    ),
                    MessageTemplateAction(
                        label='專長',
                        text='專長'
                    ),

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
                thumbnail_image_url='https://i.imgur.com/2UaRtwH.jpg',
                actions=[
                    MessageTemplateAction(
                        label='PTT熱門文章',
                        text='熱門文章'
                    )

                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
