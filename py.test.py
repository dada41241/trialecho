from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('yeWClHzSjXDo5GP+RkpVUSrXfPvmMtlf0aMBGKXrYnR7nFahp6kejv5C3LgQfxqBya4gVJdpOemwKAHVAc75a931ZMuV+UB3HCxEnhc46xAhWFl9kb18fAzhDx6yWk17sOuE6aQkbY9wdRJAJSZruwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('af064e8c91676b333ad4cc418bec7084')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()