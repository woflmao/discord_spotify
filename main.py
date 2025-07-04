import os
import asyncio
import random

import discord
from dotenv import load_dotenv

import spotipy

from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')
SPOTIFYID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFYSECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
PLAYLISTID = os.getenv('SPOTIFY_PLAYLIST_ID')
SPOTIFY_REFRESH_TOKEN = os.getenv('SPOTIFY_REFRESH_TOKEN')
REDIRECT_URI = os.getenv('REDIRECT_URI')


# Default intents are now required to pass to Client
# intents = discord.Intents.all()
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

async def authenticate_user():
  oauth = SpotifyOAuth(
    client_id=SPOTIFYID,
    client_secret=SPOTIFYSECRET,
    redirect_uri="http://127.0.0.1:8080/callback",
    scope=['playlist-modify-public']
  )

  token_info = oauth.refresh_access_token(SPOTIFY_REFRESH_TOKEN)
  access_token = token_info["access_token"]

  return spotipy.Spotify(auth=access_token)
  # return spotipy.Spotify(oauth_manager=auth)

async def add_song_to_playlist(song_url):
    # auth = SpotifyOAuth(
    #   client_id=SPOTIFYID,
    #   client_secret=SPOTIFYSECRET,
    #   redirect_uri="http://127.0.0.1:8080/callback",
    #   scope=['playlist-modify-public'],
    #   open_browser=False
    # )
    # sp = spotipy.Spotify(oauth_manager=auth)
    sp = await authenticate_user()

    # Extract the song id from the song url
    song_id = song_url.split('track/')[1]
    song_id = song_id.split('?')[0]
    song_id = ("spotify:track:" + song_id)
    print(song_id)

    # Add the song to the playlist
    # await asyncio.sleep(0)
    print(f'playlist id: {PLAYLISTID}')
    print(f'items: {[song_id]}')
    sp.playlist_add_items(playlist_id=PLAYLISTID, items=[song_id], position=None)

    # Getting the song name for message formatting, uncomment for message
    # track_id = song_id.split(':')[2]
    # track = sp.track(track_id)
    # track_name = track['name']
    # print(track_name)
    # return track_name




@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    await authenticate_user()

@client.event
async def on_message(message):
    if message.channel.id == int(CHANNEL_ID):
      if message.author == client.user:
          return
      if message.content.startswith('https://open.spotify.com/track/'):
          print(f'found message! {message.content}')
          
          # use this for no confirmation message
          await add_song_to_playlist(message.content)

          # use this for confirmation message
          # track_name = await add_song_to_playlist(message.content, PLAYLISTID)
          # embed = discord.Embed(title=f"Adding '" + track_name + "' to my playlist.", color=0x00ff00)
          # await message.channel.send(embed=embed)


client.run(DISCORD_TOKEN)