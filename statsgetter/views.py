from django.shortcuts import render
from django.http import HttpResponse
from .youtube_bundle import YoutubeBundle
from .models import *
import datetime
import openpyxl
from django.utils.timezone import localtime

# Create your views here.
def home(request):
    channels_stats = []
    if request.method == "POST":
        # get searched channel titles and make a list of channel titles
        channel_titles_str = request.POST['search']
        channel_titles = channel_titles_str.split('、')

        # when users first visit the website
        # this prevents the users to wait when they first visit the website
        if not channel_titles:
            pass
        # when users search
        else:
            stats_last = Statistics.objects.latest('id')
            last_transaction_id = stats_last.transaction_id

            # get stats for the serached channel titles
            for channel_title in channel_titles:
                yt = YoutubeBundle(channel_title)
                results = yt.get_stats_bundle()
                for result in results:
                    registered_date = datetime.datetime.strptime(result["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
                    registered_date = registered_date.strftime("%Y-%m-%d")
                    channel_stats = {
                        'title' : result["snippet"]["title"],
                        'id' : result["id"],
                        'registered_date' : registered_date,
                        'subscriberCount' : result["statistics"]["subscriberCount"],
                        'viewCount' : result["statistics"]["viewCount"],
                        'videoCount' : result["statistics"]["videoCount"],
                    }
                    channels_stats.append(channel_stats)

                    # store channel data in the database
                    youtube_channel = YoutubeChannel.objects.get_or_create(
                        title=channel_stats["title"],
                        channel_id=channel_stats["id"]
                        )

                    # store stats data in the database
                    new_stats = Statistics(
                        subscriber_count=channel_stats["subscriberCount"],
                        view_count=channel_stats["viewCount"],
                        video_count=channel_stats["videoCount"],
                        channel_registered=registered_date
                        )

                    channel = YoutubeChannel.objects.get(channel_id=channel_stats["id"])
                    new_stats.channel = channel

                    new_stats.transaction_id = last_transaction_id + 1
                    new_stats.save()

    context = {'channels_stats': channels_stats}
    return render(request, 'statsgetter/home.html', context)

def export_excel(request):
    # django setting to export excel
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Youtube_Stats_' + str(datetime.date.today()) + '.xlsx'

    # open excel
    wb = openpyxl.Workbook()
    ws = wb.active

    # only get the latest data
    stats_last = Statistics.objects.latest('id')
    last_transaction_id = stats_last.transaction_id
    stats_latest = Statistics.objects.filter(transaction_id=last_transaction_id)

    # the 1st row is for title
    ws['A1'] = 'チャンネル名'
    ws['B1'] = 'チャンネル登録日'
    ws['C1'] = 'チャンネル登録者数'
    ws['D1'] = '総再生数'
    ws['E1'] = '総動画数'
    ws['F1'] = 'データ取得日'

    # store data
    row = 2
    for data in stats_latest:
        # adjust datetime to excel format
        channel_registered_excel = data.channel_registered.strftime('%m/%d/%Y')
        date_added_excel = localtime(data.date_added).strftime('%m/%d/%Y %H:%M')

        # store data
        ws.cell(row=row, column=1).value = data.channel.title
        ws.cell(row=row, column=2).value = channel_registered_excel
        ws.cell(row=row, column=3).value = data.subscriber_count
        ws.cell(row=row, column=4).value = data.view_count
        ws.cell(row=row, column=5).value = data.video_count
        ws.cell(row=row, column=6).value = date_added_excel
        row += 1

    wb.save(response)

    return response
