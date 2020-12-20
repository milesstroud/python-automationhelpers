#IMPORTS
import praw #Reddit API Package (https://praw.readthedocs.io/en/latest/index.html)
import datetime as dt
from datetime import date
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import random

SPOTIPY_CLIENT_ID = '2cfb716804634481b678117914a9d6cd'
secret = 'ecb207bc67d14a71a2841fbdef1bff6c'
redirect_uri = 'http://localhost'
username = '1211908926'

scope = 'playlist-modify-public'
token = SpotifyOAuth(scope=scope,username=username, client_id=SPOTIPY_CLIENT_ID,client_secret=secret, redirect_uri=redirect_uri)
sp = spotipy.Spotify(auth_manager=token)

tracks = []


#PRAW Read Only Instance (https://praw.readthedocs.io/en/latest/getting_started/quick_start.html)
reddit = praw.Reddit(client_id = 'w4dmPyZu0rVYOw',
                     client_secret = 'mVwazkh1iKvNtMoBiH-GrAs4KmE',
                     user_agent = 'favorite tunes by /u/snootify')

#Dictionary to store all of the data retrieved
master_dict = {"url": []}


#Defining functions to build the master dictionary using data from each subreddit
def Pop():
    popreddit = reddit.subreddit('Popheads') #Defining subreddit of choice (first, popheads)
    popemergencies = popreddit.top(limit =25, time_filter = 'day') #Retrieving the top 5 posts within the last 24hours
    for post in popemergencies:
        master_dict['url'].append(post.url)

#Repeat for Subs of Choice!
def HipHop():
    hiphopheads = reddit.subreddit('hiphopheads')
    HHH = hiphopheads.top(limit=30, time_filter = 'day')
    for post in HHH:
        master_dict['url'].append(post.url)


def PsychRock():
    psychrock = reddit.subreddit('psychedelicrock')
    psychposts = psychrock.top(limit=20, time_filter = 'day')
    for post in psychposts:
        master_dict['url'].append(post.url)

def PCmusic():
    pcmusic = reddit.subreddit('pcmusic')
    pcposts = pcmusic.top(limit=10, time_filter = 'day')
    for post in pcposts:
        master_dict['url'].append(post.url)

def convert(tracks):
    return tuple(tracks)

#Calling each function to perform their duties before creating the email
Pop()
HipHop()
PsychRock()
PCmusic()

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


#Need first 23 characters (the length of a track id) to control for a quirk with playlist tracks
# tracks = [[track[0:22]] for track in tracks]
tracks = [track[0:22] for track in tracks]



#50 Random songs to not have long albums take up space
if len(tracks) > 50:
    tracks = random.sample(tracks, 50)
else:
    tracks = tracks

tracks = convert(tracks)
sp.playlist_add_items('2X7dRDEE3rFzSS7Opipohb', tracks)

#To Replace Instead of Add New, Uncomment This:
# sp.playlist_replace_items('2X7dRDEE3rFzSS7Opipohb', tracks)

