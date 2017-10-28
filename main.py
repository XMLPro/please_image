from flask import Flask, request, abort
import os
import search

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageSendMessage
)

app = Flask(__name__)

# line_bot_api = LineBotApi(os.environ.get('TOKEN'), "")
# handler = WebhookHandler(os.environ.get('SECRET'), "")

@app.route("/", methods=['GET'])
def hello():
    return "hello"
<<<<<<< HEAD
#
# @app.route("/callback", methods=['POST'])
# def callback():
#     # get X-Line-Signature header value
#     signature = request.headers['X-Line-Signature']
#
#     # get request body as text
#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)
#
#     # handle webhook body
#     try:
#         handler.handle(body, signature)
#     except InvalidSignatureError:
#         abort(400)
#
#     return 'OK'
#
# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     request = event.message.text
#     if request.startswith("plz"): #特定の文字列から始まるなら
#         result = request.split(" ")[1]
#         url = search.one(result)
#         image_message = ImageSendMessage(
#             original_content_url=url,
#             preview_image_url=url
#         )
#         line_bot_api.reply_message(event.reply_token,image_message)
#
#
=======

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
    request = event.message.text
    if request.startswith("plz"): #特定の文字列から始まるなら
        result = request.split(" ")[1]
        url = search.one_include_http(result, request.url_root)
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        line_bot_api.reply_message(event.reply_token,image_message)

    # そうじゃないならとりあえず何もしない

>>>>>>> e3507a2fa9200b33ca9a7c8306ec5099e45ee397
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",5000)))
