LIN,ZI-CHAO's Chatbot
=====================
for Line's interview


Runtime Environment
--------
* Python 3.6.2

Cloud Platform
--------------
* Heroku

Configuration
-------------
You have to Config Variables "ACCESS_TOKEN" and "SECRET" in Heroku

```python
  # Channel Access Token
  line_bot_api = LineBotApi(os.environ.get('ACCESS_TOKEN'))
  # Channel Secret
  handler = WebhookHandler(os.environ.get('SECRET'))
```

Usage
-----

License
-------
Licensed under the [MIT License](LICENSE.txt).
