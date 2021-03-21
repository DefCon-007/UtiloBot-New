import json
import requests
import os
import sentry_sdk
from utilobot.helper import make_request
# from sentry_sdk.integrations.gcp import GcpIntegration
from utilobot.bot_functionalities import SongParser, TelegramParseCallbackQueryData, URLShortner
from random import randint
from utilobot.exceptions import BaseFunctionalityException
from sentry_sdk import capture_exception

# sentry_sdk.init(
#     os.environ.get('SENTRY_DSN'),
#     integrations=[GcpIntegration()],
#     traces_sample_rate=1.0,
# )

TELE_TOKEN = os.environ['BOT_TOKEN']
URL = "https://api.telegram.org/bot{}/".format(TELE_TOKEN)



def sendChatAction(chat_action, chat_id): 
    assert chat_action in ['typing', 'upload_photo', 'record_video', 'upload_video', 
                           'record_audio', 'upload_audio', 'upload_document', 'find_location', 
                           'record_video_note', 'upload_video_note'], "Unidentified chat action detected!"
    args = {}
    args['chat_id'] = chat_id
    args['action'] = chat_action
    request, session = make_request("post", URL+"sendChatAction", None, {'json': args})


def send_message(text, chat_id, args={}):
    args['chat_id'] = chat_id
    args['text'] = text
    if "parse_mode" not in args: 
        args['parse_mode'] = "HTML"
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

def parse_bot_commands(command, chat_id, body): 
    clean_command = command.lower()
    if "/song" in clean_command:
        # The user wants to parse the song URL
        sendChatAction('typing', chat_id)
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
        
    elif "/short" in clean_command: 
        # The user wants to shorten a URL 
        url_shortner_object = URLShortner(command)
        short_url = url_shortner_object.get_short_url()
        message = "The shortend URL for the provided link is {}".format(short_url)
        send_message(message, chat_id)
    
    elif "/start" in clean_command: 
        # The starting message send to the user
        welcome_message_1 = [
        "Hi ",
        "Hola ",
        "Hey ",
        "Hey there, "
        ]

        welcome_message_2 = [
        "! Looks like we haven't met before.",
        "! Looks like this is our first meet.",
        "! How are you doing.",
        ]

        welcome_message_3 = [
        " Send /help to know my secrets."
        ]
        message = body.get('message')
        name = None
        if message and message.get('chat'): 
            chat = message['chat']
            if chat.get('type') == "private": 
                name = chat.get('first_name')
        rand_index1 = randint(0,len(welcome_message_1) -1)
        rand_index2 = randint(0,len(welcome_message_2) -1)
        rand_index3 = randint(0,len(welcome_message_3) -1)
        if name: 
            msg1 = welcome_message_1[rand_index1] + name
        else: 
            msg1 = welcome_message_1[rand_index1][:-1]
        msg = msg1 + welcome_message_2[rand_index2]+ welcome_message_3[rand_index3]
        send_message(msg, chat_id)	
    
    elif "/help" in clean_command: 
        help_message = "Following are the commands and usages for the bot.\n\n" \
        "<strong>1. Convert songs form one streaming service to others</strong>\n" \
        "Just use the command /song along with the URL of the song and receive links of the same song on other services.\n" \
        "For e.g. /song https://www.youtube.com/watch?v=w2Ov5jzm3j8\n\n" \
        "<strong>2. Get random jokes</strong>\n" \
        "Send /joke and follow the onscreen instructions to receive the jokes.\n\n" \
        "<strong>3. Shorten a URL</strong>\n" \
        "Use the command /short and send the URL you wish to shorten and receive a short URL instantly." \
        "For e.g. /short https://www.google.com"
        send_message(help_message, chat_id, {"disable_web_page_preview": True})
        
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
                parse_bot_commands(msg.get('text'), chat_id, body)
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
    
def lambda_handler(request):
    body = request.get_json()
    print(body)
    chat_id = get_chat_id_from_body(body)
    try:
        parse_incoming_request(body, chat_id)
    except BaseFunctionalityException as e:
        # capture_exception(e)
        send_message(e.return_msg, chat_id)
    except Exception as e: 
        # capture_exception(e)
        send_message("Some internal error occurred! Please try again later.", chat_id)
    return {
        'statusCode': 200
    }
