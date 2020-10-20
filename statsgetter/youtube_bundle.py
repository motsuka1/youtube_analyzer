from .youtube_statistics import YTstats
from .youtube_scraper import YTscraper
import environ
from .models import *

class YoutubeBundle:
    def __init__(self, channel_title):
        self.channel_title = channel_title

    def get_stats_bundle(self):
        env = environ.Env()
        environ.Env.read_env()

        API_KEY = env('API_KEY')

        # check if channel_title exists in the database
        # if so, retrieve channel_id
        if YoutubeChannel.objects.filter(title__exact=self.channel_title).exists():
            youtube_channel = YoutubeChannel.objects.filter(title__exact=self.channel_title).get()
            channel_id = youtube_channel.channel_id
            channel_username = None
        else:
            # get channel_id or channel_username by running selenium
            ytscraper = YTscraper(self.channel_title)
            channel_data = ytscraper.get_channel_id_or_username_from_title()

            # identify if returned data is channel_id or channel_username
            if channel_data[0] == True:
                channel_id = channel_data[1]
                channel_username = None
            else:
                channel_id = None
                channel_username = channel_data[1]

        # get stats by using youtube api
        ytstats = YTstats(API_KEY, channel_id, channel_username)
        data = ytstats.get_channel_statistics()
        return data
