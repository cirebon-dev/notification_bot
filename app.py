# -*-coding:utf8;-*-
from cryptography.fernet import Fernet
from bottle import route, request, post, auth_basic
import json
import requests
import bottle
import telegram
import os
"""
Telegram notification bot with highly privacy/data protection.
author: guangrei
"""

HOST = os.environ.get("TG_BOT_HOST")
ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY")
admin_user = os.environ.get("ADMIN_USER")
admin_password = os.environ.get("ADMIN_PASSWORD")
template = """
now you can start sending messages, for example:
`curl -X POST https://end-points -d '{"text": "Hello, world 🐣"}'`
"""
help_template = """
to get support please open issues <a href="https://github.com/cirebon-dev/notification_bot">here</a>
and follow our channel @anak_tkj
"""
key = ENCRYPTION_KEY.encode()
fernet = Fernet(key)


def is_authenticated_user(user, password):
    return user == admin_user and password == admin_password


@route('/')
def root_handler():
    return "its works!"


@route("/update_webhook")
@auth_basic(is_authenticated_user)
def update_handler():
    url = f'https://{HOST}/{telegram.token.replace(":","_")}'
    return telegram.set_webhook(url)


@post('/'+telegram.token.replace(":", "_"))
def telegram_hook():
    data = request.json
    msg = telegram.get_message(data)
    msg_id = telegram.get_message_id(data)
    chat_id = telegram.get_chat_id(data)
    if msg == "/start":
        token = fernet.encrypt(str(chat_id).encode())
        msg = f"{HOST}/h/{token.decode()}"
        msg = template.replace("end-points", msg)
        telegram.send_message(
            msg, chat_id, parse_mode="Markdown", disable_web_page_preview=True, reply_to_message_id=msg_id)
    elif msg == "/help":
        telegram.send_message(help_template, chat_id, parse_mode="Html",
                              reply_to_message_id=msg_id)

    return "OK"


@post('/h/<token>')
def notify_handler(token):
    try:
        data = request.body.read().decode('utf-8')
        data = json.loads(data)
        chat_id = int(fernet.decrypt(token.encode()).decode())
        return telegram.send_message(data["text"], chat_id)
    except BaseException as e:
        return {"ok": False, "ServerError": str(e)}


bottle.debug(True)
app = application = bottle.default_app()

if __name__ == "__main__":
    bottle.run(host='0.0.0.0', port=80, debug=True)
