from flask import Flask, request, abort
from linebot import (
        LineBotApi, WebhookHandler
)
from linebot.exceptions import (
        InvalidSignatureError
)
from linebot.models import *

import os
import crawler

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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    #print(event.source.user_id)

    if event.message.text == "PTT熱門文章":
        content = crawler.ptt_hot()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
        return 0

    if event.message.text == "Youtube熱門影片":
        content = crawler.youtube_hot()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
        return 0

    if event.message.text == "Dcard熱門文章":
        content = crawler.dcard_hot()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
        return 0

    #Debugging
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
                        label='專業技能',
                        text='專業技能'
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

    if event.message.text == "所有功能":
        carousel_template = TemplateSendMessage(
            alt_text='所有功能 目錄',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        title='額外功能',
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
                    ),
                    CarouselColumn(
                        title='額外功能',
                        text='請選擇',
                        thumbnail_image_url='https://i.imgur.com/EuRHQUt.jpg',
                        actions=[
                            URITemplateAction(
                                label='Cigarette Smokers Problem',
                                uri='https://github.com/linzichao/OS_smoker'
                            ),
                            URITemplateAction(
                                label='Dcard熱門文章',
                                uri='Dcard熱門文章'
                            ),
                            URITemplateAction(
                                label='Wake Up At Dawn',
                                uri='https://linzichao.github.io/3D_final/'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template)
        return 0


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
