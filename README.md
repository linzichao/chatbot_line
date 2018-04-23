LIN,ZI-CHAO's(林資超) Chatbot
=====================
for Line's interview


Runtime Environment
--------
* Python 3.6.2

Cloud Platform
--------------
* Heroku


How to Use
-----

You can add ZI-CHAO's Chatbot as a friend by LINE@ QRCode.

<img src="https://i.imgur.com/67dM9oL.jpg" width="250" height="250"/>

When you add ZI-CHAO's Chatbot as a friend, the Chatbot will send you a greeting message. Furthermore, you will see a button menu below.

<img src="https://i.imgur.com/dNsIFcz.jpg" width="300" height="500"/>

If you click the button "了解資超", Chatbot will send you personal infomation menu about ZI-CHAO.

<img src="https://i.imgur.com/CX9UH4s.jpg" width="300" height="450"/>

If you click the button "所有功能", Chatbot will send you the menu of all extra features.

<img src="https://i.imgur.com/JtmvxFX.jpg" width="300" height="450"/>

How to Build your own Chatbot
-----------------------------

### Preparation
* [Getting Started on Heroku with Python](https://devcenter.heroku.com/articles/getting-started-with-python#introduction)
* [Getting Started with the Messaging API ](https://developers.line.me/en/docs/messaging-api/getting-started/)
* Clone the codes & Push to Heroku

### Configuration

You have to set Config Variables "ACCESS_TOKEN" and "SECRET" in Heroku.

```python
  # Channel Access Token
  line_bot_api = LineBotApi(os.environ.get('ACCESS_TOKEN'))
  # Channel Secret
  handler = WebhookHandler(os.environ.get('SECRET'))
```

### Setting your own message

You can set your Chatbot's keyword response in LINE@ MANAGER.

<img src="https://i.imgur.com/mmV8XnZ.jpg" width="600" />

You can also set your Chatbot's richmenu in LINE@ MANAGER.

<img src="https://i.imgur.com/L1GtuoV.jpg" width="600" />

Reference
---------
* [line-bot-sdk-python](https://github.com/line/line-bot-sdk-python)

License
-------
Licensed under the [MIT License](LICENSE.txt).
