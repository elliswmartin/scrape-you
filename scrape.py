#!/usr/bin/env python3

import scrapetube
import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import argparse
import time

# get current time for unique filename
timestr = time.strftime("%Y%m%d-%H%M%S") 

# add parser for easy command line calls
parser = argparse.ArgumentParser()
parser.add_argument("term1", help="first term to search")
parser.add_argument("term2", help="second term to search")
parser.add_argument("channel_id", help="find using Share arrow on a YouTube Channel's About page ex: 'UCk5gEr_7yZ-XKsX57qKZ1bw'")
args = parser.parse_args()

# make list of videos from channel 
videos = scrapetube.get_channel(args.channel_id)
video_list = []
print("Gathering list of videos")

# make list of all video IDs
for video in videos:
    video_list.append(video['videoId'])

# get transcripts and perform regular expression search
pattern = "(" + str(args.term1) + ")|(" + str(args.term2) + ")"
formatter = TextFormatter()
match_list = []

# loop through videos in list
print("Searching for " + pattern + " in transcripts.")
for video in video_list:
    # get transcript of video 
    try:
        trans_dict = YouTubeTranscriptApi.get_transcript(video)
        trans_txt = formatter.format_transcript(trans_dict)
        # perform regex search
        result = re.findall(pattern, trans_txt)
        # if pattern found, append to match list
        if result:
            print(video + ": " + str(result))
            match_list.append(video)
    except:
        print("Neither word found: " + video)

# save matches to .txt file
print("Search complete, saving matches to .txt file.")
filename = "match_list_" + str(timestr)+ ".txt"
with open(filename, "w") as output:
    output.write(str(match_list))