import requests
import json

class YTstats:
    def __init__(self, api_key, channel_id, channel_username):
        self.api_key = api_key
        self.channel_username = channel_username
        if channel_id == None:
            self.channel_id = self.get_channel_id_from_username()
        else:
            self.channel_id = channel_id

    def get_channel_statistics(self):
        url = f'https://www.googleapis.com/youtube/v3/channels?id={self.channel_id}&key={self.api_key}&part=statistics,snippet&fields=items(id,snippet(title,publishedAt),statistics(viewCount,subscriberCount,videoCount))'
        json_url = requests.get(url)
        data = json.loads(json_url.text)["items"]
        return data

    def get_channel_id_from_username(self):
        url = f'https://www.googleapis.com/youtube/v3/channels?part=id&forUsername={self.channel_username}&key={self.api_key}&fields=items(id)'
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        channel_id = data["items"][0]["id"]
        return channel_id
