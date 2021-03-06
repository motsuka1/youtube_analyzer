from django.db import models

# Create your models here.
class YoutubeChannel(models.Model):
    title = models.CharField(max_length=100)
    channel_id = models.CharField(max_length=25)

    def __str__(self):
        return self.title

class Statistics(models.Model):
    channel = models.ForeignKey(YoutubeChannel, on_delete=models.CASCADE)
    subscriber_count = models.IntegerField(default=0, null=True, blank=True) # null&blank are true for the case when subscriber is hidden
    view_count = models.BigIntegerField(default=0)
    video_count = models.IntegerField(default=0)
    channel_registered = models.DateField()
    date_added = models.DateTimeField(auto_now_add=True)
    transaction_id = models.IntegerField(default=0)

    def __str__(self):
        return str(self.transaction_id)

class Nickname(models.Model):
    channel = models.ForeignKey(YoutubeChannel, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.nickname
