from django.shortcuts import render
from .youtube_bundle import YoutubeBundle
from .models import *
import datetime

# Create your views here.
def home(request):
    channel_title = "python enginner"
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
    context = {'channel_stats': channel_stats}
    return render(request, 'statsgetter/home.html', context)
