# -*-coding:utf8;-*-
from cryptography.fernet import Fernet
from bottle import route, request, post, auth_basic, hook, response
import bottle
import json
import bottle
import telegram
import os

"""
Telegram notification bot with highly privacy/data protection.
author: guangrei
"""

# bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024 # un-comment this to change default request limit!
HOST = os.environ.get("TG_BOT_HOST")
ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY")
admin_user = os.environ.get("ADMIN_USER")
admin_password = os.environ.get("ADMIN_PASSWORD")
start_template = """
Your token is `{token}`
You are now ready to start sending messages, please check /help\_send\_text and /help\_send\_file to get started!
"""
help_send_text_template = """
** ENDPOINTS: **
`https://end-points`

** METHOD: ** `POST`

** BODY: **
`{
  "text": "message text (required)"
}`

example:
`curl -X POST https://end-points -d '{"text": "Hello, world 🐣"}'`
"""
help_send_file_template = """
** ENDPOINTS: **
`https://end-points`

** METHOD: ** `POST`

** BODY: **
`{
  "file": {
    "name": "file name with extension (required)",
    "content": "base64 file content (required)",
    "caption": "file caption (optional)"
  }
}`

example:
`echo "this is test file!" > test_file.txt && curl -X POST https://end-points -d "{\\"file\\": {\\"name\\": \\"test_file.txt\\", \\"content\\": \\"$(base64 -w 0 < test_file.txt)\\"}}"`
"""
help_template = """
to get support please open issues <a href="https://github.com/cirebon-dev/notification_bot">here</a>
and follow our channel @anak_tkj
"""
_allow_origin = "*"
_allow_methods = "PUT, GET, POST, DELETE, OPTIONS"
_allow_headers = "Authorization, Origin, Accept, Content-Type, X-Requested-With"
key = ENCRYPTION_KEY.encode()
fernet = Fernet(key)


def is_authenticated_user(user, password):
    return user == admin_user and password == admin_password


@hook("after_request")
def enable_cors():
    response.headers["Access-Control-Allow-Origin"] = _allow_origin
    response.headers["Access-Control-Allow-Methods"] = _allow_methods
    response.headers["Access-Control-Allow-Headers"] = _allow_headers


@route("/", method="OPTIONS")
@route("/<path:path>", method="OPTIONS")
def options_handler(path=None):
    return


@route("/")
def root_handler():
    return "its works!"


@route("/update_webhook")
@auth_basic(is_authenticated_user)
def update_handler():
    url = f'https://{HOST}/{telegram.token.replace(":","_")}'
    return telegram.set_webhook(url)


@post("/" + telegram.token.replace(":", "_"))
def telegram_hook():
    data = request.json
    msg = telegram.get_message(data)
    msg_id = telegram.get_message_id(data)
    chat_id = telegram.get_chat_id(data)
    token = fernet.encrypt(str(chat_id).encode())
    api_uri = f"{HOST}/h/{token.decode()}"
    if msg == "/start":
        msg = start_template.format(token=token.decode())
        telegram.send_message(
            msg,
            chat_id,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_to_message_id=msg_id,
        )
    elif msg == "/help_send_text":
        msg = help_send_text_template.replace("end-points", api_uri)
        telegram.send_message(
            msg,
            chat_id,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_to_message_id=msg_id,
        )
    elif msg == "/help_send_file":
        msg = help_send_file_template.replace("end-points", api_uri)
        telegram.send_message(
            msg,
            chat_id,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_to_message_id=msg_id,
        )
    elif msg == "/help":
        telegram.send_message(
            help_template, chat_id, parse_mode="Html", reply_to_message_id=msg_id
        )

    return "OK"


@post("/h/<token>")
def notify_handler(token):
    try:
        data = request.body.read().decode("utf-8")
        data = json.loads(data)
        chat_id = int(fernet.decrypt(token.encode()).decode())
        if "text" in data:
            return telegram.send_message(data["text"], chat_id)
        if "file" in data:
            if "caption" in data["file"]:
                return telegram.send_file(
                    data["file"]["name"],
                    data["file"]["content"],
                    chat_id,
                    data["file"]["caption"],
                )
            else:
                return telegram.send_file(
                    data["file"]["name"], data["file"]["content"], chat_id
                )
    except BaseException as e:
        return {"ok": False, "ServerError": str(e)}


bottle.debug(True)
app = application = bottle.default_app()

if __name__ == "__main__":
    bottle.run(host="0.0.0.0", port=80, reloader=True)
