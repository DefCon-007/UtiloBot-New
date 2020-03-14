import json
import requests
import os
import sentry_sdk
from helper import make_request
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration
from bot_functionalities import SongParser, TelegramParseCallbackQueryData
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
        joke_buttons = [[{'text':"Chuch Norris nerdy joke" , 'callback_data' : 'JOKE_CHUCKN_nerdy'}],[{'text':'Chuch Norris explicit joke' , 'callback_data' : 'JOKE_CHUCKN_explicit'}]]
        send_inline_keyboard(message, chat_id, "inline_keyboard", joke_buttons)
        
    else:
        send_message("Unknown command! Please try again", chat_id)
    
def parse_incoming_request(body, chat_id):
    if 'message' in body: 
        # Parse the message reply
        msg = body.get('message')
        entities = msg.get('entities')
        if entities: 
            entities_list = [entity['type'] for entity in entities if entity.get("type")] # Get list of all entity types 
            
            # Parse entity types in precedance order
            if "bot_command" in entities_list: 
                parse_bot_commands(msg.get('text'), chat_id)
    if 'callback_query' in body: 
        # Parse the callback query
        callback_query = body.get('callback_query')
        data = callback_query.get('data')
        if data:
            data_list = data.split("_")
            callback_query_parser_object = TelegramParseCallbackQueryData(data_list)
            text, args =  callback_query_parser_object.parse()
            send_message(text, chat_id, args)
    # else:
    # if msg and msg.get('text'):
    #     parse_user_text(msg['text'].strip(), chat_id)

def get_chat_id_from_body(body): 
    if 'message' in body: 
        return body['message']['chat']['id']
    if 'callback_query' in body: 
        return body['callback_query']['message']['chat']['id']
    
def lambda_handler(event, context):
    print(event)
    if not isinstance(event['body'], dict):
        body = json.loads(event['body'])
    else:
        body = event['body']
    chat_id = get_chat_id_from_body(body)
    try:
        parse_incoming_request(body, chat_id)
    except BaseFunctionalityException as e:
        send_message(e.return_msg, chat_id)
    return {
        'statusCode': 200
    }
