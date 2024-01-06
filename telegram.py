# -*-coding:utf8;-*-
import os
import requests
"""
library to interact with telegram bot api
references:
- https://telegram-bot-sdk.readme.io/reference/sendmessage
- https://djangostars.com/blog/how-to-create-and-deploy-a-telegram-bot/
"""

token = os.environ.get("TG_BOT_TOKEN")
BOT_URL = f'https://api.telegram.org/bot{token}/'


def get_chat_id(data):
    chat_id = data['message']['chat']['id']
    return chat_id

def get_message(data):
    message_text = data['message']['text']
    return message_text

def get_message_id(data):
    message_id = data['message']['message_id']
    return message_id
    
def send_message(text, chat_id, parse_mode=False, disable_web_page_preview=False, disable_notification=False, reply_to_message_id=False, reply_markup=False):
    message_url = BOT_URL + 'sendMessage'
    json_data = {"chat_id": chat_id, "text": text, "disable_web_page_preview":
                 disable_web_page_preview, "disable_notification": disable_notification}
    if parse_mode:
        json_data['parse_mode'] = parse_mode
    if reply_to_message_id:
        json_data["reply_to_message_id"] = reply_to_message_id
    if reply_markup:
        json_data["reply_markup"] = reply_markup
    return requests.post(message_url, json=json_data).json()


def set_webhook(uri):
    api = BOT_URL + 'setWebHook?url='+uri
    return requests.get(api).json()
