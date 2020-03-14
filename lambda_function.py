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


def parse_user_text(msg_text, chat_id):
    send_message("Unknown message! Please try again", chat_id)

def parse_bot_commands(command, chat_id): 
    clean_command = command.lower()
    if "/song" in clean_command:
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

    elif "/joke" in clean_command: 
        # The user wants to hear a joke
        message = "Select which joke you want!"
        joke_buttons = [[{'text':"Chuch Norris nerdy joke" , 'callback_data' : 'joke_CN_nerdy'}],[{'text':'Chuch Norris explicit joke' , 'callback_data' : 'joke_CN_explicit'}]]
        send_inline_keyboard(message_text, chat_id, "inline_keyboard", joke_buttons)
        
    else:
        send_message("Unknown command! Please try again", chat_id)
    
def parse_incoming_request(data, chat_id):
    msg = data.get('message')
    entities = msg.get('entities')
    if entities: 
        entities_list = [entity['type'] for entity in entities if entity.get("type")] # Get list of all entity types 
        
        # Parse entity types in precedance order
        if "bot_command" in entities_list: 
            parse_bot_commands(msg.get('text'), chat_id)
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
