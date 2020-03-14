import json
import requests
import os
import sentry_sdk
from helper import make_request
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration
from bot_functionalities import SongParser
from exceptions import BaseFunctionalityException

sentry_sdk.init(
    os.environ.get('SENTRY_DSN'),
    integrations=[AwsLambdaIntegration()]
)

TELE_TOKEN = os.environ['BOT_TOKEN']
URL = "https://api.telegram.org/bot{}/".format(TELE_TOKEN)


def send_message(text, chat_id, args={}):
    args['chat_id'] = chat_id
    args['text'] = text
    request, session = make_request("post", URL+"sendMessage", None, {'json': args})


def send_inline_keyboard(text, chat_id, reply_markup, data):
    args = {
        "reply_markup": {
            reply_markup: data
            }
    }
    send_message(text, chat_id, args)


def handle_commands(command, chat_id):
    if "song" in command.lower():
        # The user wants to parse the song URL
        song_object = SongParser(command)
        data_list = song_object.convert_song()
        song_open_button = []
        for data in data_list["links"]: 
            song_open_button.append([{
                "text": "Open on {}".format(data['service_name']),
                "url": data['link']
            }])
        message_text = "Select your desired music service for {} from below.".format(data_list['name'])
        send_inline_keyboard(message_text, chat_id, "inline_keyboard", song_open_button)

    else:
        send_message("Unknown command! Please try again", chat_id)


def parse_user_text(msg_text, chat_id):
    if msg_text[0] == "/":
        # Starts with a slash. process the command
        handle_commands(msg_text[1:], chat_id)

    else:
        send_message("Unknown message! Please try again", chat_id)


def parse_incoming_request(data, chat_id):
    msg = data.get('message')
    if msg and msg.get('text'):
        parse_user_text(msg['text'].strip(), chat_id)


def lambda_handler(event, context):
    print(event)
    if not isinstance(event['body'], dict):
        message = json.loads(event['body'])
    else:
        message = event['body']
    chat_id = message['message']['chat']['id']
    try:
        parse_incoming_request(message, chat_id)
    except BaseFunctionalityException as e:
        send_message(e.return_msg, chat_id)
    return {
        'statusCode': 200
    }
