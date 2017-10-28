from flask import Flask, request, abort
import os

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

line_bot_api = LineBotApi(os.environ.get('TOKEN'))
handler = WebhookHandler(os.environ.get('SECRET'))

@app.route("/", methods=['GET'])
def hello():
    return "hello"

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
    result = "default"
    if request.startswith("plz"): #特定の文字列から始まるなら
        result = request.split(" ")[1]
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=result))

    image_message = ImageSendMessage(
        original_content_url='https://pbs.twimg.com/media/DL3N2v2UEAAO_9_.jpg',
        preview_image_url='https://pbs.twimg.com/media/DL3N2v2UEAAO_9_.jpg'
    )
    line_bot_api.reply_message(event.reply_token,image_message)


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",5000)))