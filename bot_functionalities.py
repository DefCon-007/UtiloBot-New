import requests
import json
from commonregex import CommonRegex
from exceptions import *
from helper import make_request
from sentry_sdk import capture_message


parser = CommonRegex()

class SongParser(object): 
    base_url = "https://songwhip.com/api/"
    headers = {
                'Origin': 'https://songwhip.com',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36 OPR/67.0.3575.53',
                'Content-Type': 'application/json'
                }
    # payload = "{\"url\":\"{}\",\"country\":\"IN\"}"
    payload = {
        "country": "IN",
        "url": ""
    }
    SONG_SERVICES_MAP = {
        "tidal": "Tidal",
        "deezer": "Deezer",
        "itunes": "iTunes",
        "pandora": "Pandora",
        "spotify": "Spotify",
        "youtube": "YouTube",
        "googleplay": "Google Play",
        "itunesStore": "iTunes Store",
        "youtubeMusic": "YouTube Music",
        "googleplayStore": "Google Play Store",
        "amazon": "Amazon",
        "amazonMusic": "Amazon Music",
        "napster": "Napster"
    }
    
    def __init__(self, command): 
        song_url = parser.links(command)
        if len(song_url) == 0: 
            raise InvalidSongURLException()
        else: 
            self.url = song_url[0]
    
    def convert_song(self): 
        self.payload['url'] = self.url
        args = {
            "headers": self.headers,
            "data": json.dumps(self.payload)
        }
        response, session = make_request("POST", self.base_url, None, args)     
        response_json = response.json()
        converted_links = []
        if response_json.get('status') == "success":
            for key, value in response_json['data']['links'].items(): 
                service_name = self.SONG_SERVICES_MAP.get(key)
                if not service_name: 
                    capture_message("Unabel to find SONG_SERVICES_MAP for {}".format(key))
                    service_name = key.title()
                converted_links.append({
                    "service_name": service_name,
                    "link": self.parse_link_response(value[0])
                })
            print(converted_links)
            links_list = sorted(converted_links, key=lambda item: item['service_name'].lower())
            return {
                "name": response_json["data"].get('name'),
                "links": links_list
            }
        else: 
            raise CannotConvertSongException()
        
    def parse_link_response(self, link_data): 
        print("Parsing link resposne ", link_data)
        if "{country}" in link_data['link']: 
            link = link_data['link'].replace("{country}", link_data['countries'][0])
        else: 
            link = link_data['link']
        return link
    
    def get_parsed_song_data(self): 
        converted_links = self.convert_song()
         
         
class Joke(object): 
    base_url = "http://api.icndb.com/jokes/random?limitTo=[{}]"
    def __init__(self):
        super().__init__()
        

    def get_chuck_norris_joke(self, category): 
        """
        category - "nerdy" or "explicit"
        """
        if category not in ['nerdy', 'explicit']: 
            InvalidChuckNorrisJokeCategory()
        base_url = "http://api.icndb.com/jokes/random?limitTo=[{}]".format(category)
        response, session = make_request("get", base_url)
        joke_json = response.json()
		joke_msg = html.unescape(joke_json['value']['joke'])  # decoding the html encoding in the joke
		return joke_msg
        