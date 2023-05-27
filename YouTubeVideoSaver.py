import os, subprocess, time
import urllib.request
import re

syntax = """-S res,ext:mp4:m4a --remux mp4"""
def DownloadVideo(link):
    print(link)
    command = "yt-dlp " + syntax + " " + link + " --write-subs --embed-subs -P " + '"' + channelName + '"'
    subprocess.run(command, shell=True)

recentVideosLimit = -1 #-1, videos as far back as the RSS feed goes
YouTubeRSS = []
with open("channelRSSLinks.txt", 'r', encoding="utf8") as f:
  YouTubeRSS = f.readlines()

# Each RSS feed URL in list
for rssURL in YouTubeRSS:
    foundChannelName = False
    channelName = "unknownChannel"
    videosDownloaded = 0
    # Retrieve the RSS feed data
    with urllib.request.urlopen(rssURL) as response:
        rssData = response.read().decode()
    # Parse the data    
    data = rssData.split('\n')
    for line in data:
        if '<title>' in line and foundChannelName == False:
            channelName = line.replace('<title>','').replace('</title>','').replace(" ", "").strip()
            foundChannelName = True
            print(channelName)
        if '<link rel="alternate"' in line and 'watch?v=' in line:
            video = line.replace('<link rel="alternate" href=','').replace('/>','').strip()
            DownloadVideo(video)
            videosDownloaded = videosDownloaded + 1
        if videosDownloaded > recentVideosLimit - 1 and recentVideosLimit > 0:
            break
