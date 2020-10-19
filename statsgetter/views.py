from django.shortcuts import render
from .youtube_bundle import YoutubeBundle
from .models import *
import datetime

# Create your views here.
def home(request):
    channels_stats = []
    if request.method == "POST":
        # make a list of channel titles
        channel_titles_str = request.POST['search']
        channel_titles = channel_titles_str.split('、')

        # when users first visit the website
        # this prevents the users to wait when they first visit the website
        if not channel_titles:
            pass
        # when users search
        else:
            for channel_title in channel_titles:
                yt = YoutubeBundle(channel_title)
                results = yt.get_stats_bundle()
                for result in results:
                    registered_date = datetime.datetime.strptime(result["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
                    registered_date = registered_date.strftime("%Y/%m/%d")
                    channel_stats = {
                        'title' : result["snippet"]["title"],
                        'id' : result["id"],
                        'registered_date' : registered_date,
                        'subscriberCount' : result["statistics"]["subscriberCount"],
                        'viewCount' : result["statistics"]["viewCount"],
                        'videoCount' : result["statistics"]["videoCount"],
                    }
                    channels_stats.append(channel_stats)
    context = {'channels_stats': channels_stats}
    return render(request, 'statsgetter/home.html', context)
