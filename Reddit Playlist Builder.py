#IMPORTS
import praw #Reddit API Package (https://praw.readthedocs.io/en/latest/index.html)
import datetime as dt
from datetime import date
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import random
import json
import requests
import re

SPOTIPY_CLIENT_ID = ''
secret = ''
redirect_uri = 'http://localhost'
username = ''

API_KEY = ''


scope = 'playlist-modify-public'
token = SpotifyOAuth(scope=scope,username=username, client_id=SPOTIPY_CLIENT_ID,client_secret=secret, redirect_uri=redirect_uri)
sp = spotipy.Spotify(auth_manager=token)

tracks = []


#PRAW Read Only Instance (https://praw.readthedocs.io/en/latest/getting_started/quick_start.html)
reddit = praw.Reddit(client_id = '',
                     client_secret = '',
                     user_agent = '')

#Dictionary to store all of the data retrieved
master_dict = {"url": []}
song_titles = []


#Function to remove URL Hostile string components
def urlify(s):

    # Remove all non-word characters (everything except numbers and letters)
    s = re.sub(r"[^\w\s]", '', s)

    # Replace all runs of whitespace with a single dash
    s = re.sub(r"\s+", '+', s)

    return s


#Defining functions to build the master dictionary using data from each subreddit
def Pop():
    popreddit = reddit.subreddit('Popheads') #Defining subreddit of choice (first, popheads)
    popemergencies = popreddit.top(limit =35, time_filter = 'day') #Retrieving the top 5 posts within the last 24hours
    for post in popemergencies:
        master_dict['url'].append(post.url)
        print(master_dict)

#Repeat for Subs of Choice!
def HipHop():
    hiphopheads = reddit.subreddit('hiphopheads')
    HHH = hiphopheads.top(limit=30, time_filter = 'day')
    for post in HHH:
        master_dict['url'].append(post.url)
        print(master_dict)


def PsychRock():
    psychrock = reddit.subreddit('psychedelicrock')
    psychposts = psychrock.top(limit=10, time_filter = 'day')
    for post in psychposts:
        master_dict['url'].append(post.url)
        print(master_dict)

def PCmusic():
    pcmusic = reddit.subreddit('pcmusic')
    pcposts = pcmusic.top(limit=15, time_filter = 'day')
    for post in pcposts:
        master_dict['url'].append(post.url)
        print(master_dict)


def indieheads():
    indieheads = reddit.subreddit('indieheads')
    indietunes = indieheads.top(limit=15, time_filter = 'day')
    for post in indietunes:
        master_dict['url'].append(post.url)
        print(master_dict)

def convert(tracks):
    return tuple(tracks)

#Calling each function to perform their duties before creating the email
Pop()
HipHop()
PsychRock()
PCmusic()
indieheads()

#Looping through either a playlist, track, or album
for url in master_dict['url']:
    if url.startswith('https://open.spotify.com/playlist/'):
        playlist_id = url[34:]
        print(playlist_id)
        for item in sp.playlist(playlist_id)['tracks']['items']:
            tracks.append(item['track']['id'])
    elif url.startswith('https://open.spotify.com/track/'):
        track_id = url[31:]
        print(track_id)
        tracks.append(track_id)
    elif url.startswith('https://open.spotify.com/album/'):
        album_id = url[31:]
        print(album_id)
        for item in sp.album(album_id)['tracks']['items']:
            tracks.append(item['id'])
    elif url.startswith('https://www.youtube.com/watch?v='):
        video_id = url[32:43]
        response = requests.get('https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id=' + video_id + '&key=' + API_KEY)
        response = json.loads(response.content)
        song_titles.append(response['items'][0]['snippet']['title'])
    elif url.startswith('https://youtu.be/'):
        video_id = url[17:28]
        response = requests.get('https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id=' + video_id + '&key=' + API_KEY)
        response = json.loads(response.content)
        song_titles.append(response['items'][0]['snippet']['title'])

#Need first 23 characters (the length of a track id) to control for a quirk with playlist tracks
# tracks = [[track[0:22]] for track in tracks]
tracks = [track[0:22] for track in tracks]



#50 Random Spotify songs to not have long albums take up space (can't add more than 50 at once)
if len(tracks) > 50:
    tracks = random.sample(tracks, 50)
else:
    tracks = tracks

tracks = convert(tracks)

#To Replace Instead of Add New, Uncomment This:
sp.playlist_replace_items('', tracks)

#TIME TO GRAB THE YOUTUBE SONGS ON SPOTIFY
tracks = []
for song in song_titles:
    song = re.sub('\(.*\)', "", song)
    song = re.sub('\[.*\]', "", song)
    results = sp.search(q=song, type='track')
    try:
        tracks.append(results['tracks']['items'][0]['id'])
    except:
        pass

if len(tracks) > 50:
    tracks = random.sample(tracks, 50)
else:
    tracks = tracks

print(tracks)
tracks = convert(tracks)
sp.playlist_add_items('2X7dRDEE3rFzSS7Opipohb', tracks)

