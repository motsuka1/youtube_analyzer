from youtube_statistics import YTstats
import environ

env = environ.Env()
environ.Env.read_env()

'''Dont forget to hide API_KEY'''
API_KEY = env('API_KEY')

# get the chnnel_id from the last part of channel url or from the html
# in the future, make a function to get channel_id by just typing channel titile (or keywords)
'''Change below accordingly'''
channel_id = None
channel_username = "TokaiOnAir"

yt = YTstats(API_KEY, channel_id, channel_username)
data = yt.get_channel_statistics()
print(data)
