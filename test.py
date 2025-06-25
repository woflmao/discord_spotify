import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# RUN THIS SCRIPT FROM A COMPUTER WITH BROWSER ACCESS TO GET ACCESS TOKEN AND REFRESH TOKEN
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')
SPOTIFYID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFYSECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
PLAYLISTID = os.getenv('SPOTIFY_PLAYLIST_ID')
SPOTIFY_REFRESH_TOKEN = os.getenv('SPOTIFY_REFRESH_TOKEN')
REDIRECT_URI = os.getenv('REDIRECT_URI')


# Step 1: Create OAuth object with no browser interaction
oauth = SpotifyOAuth(
    client_id=SPOTIFYID,
    client_secret=SPOTIFYSECRET,
    redirect_uri=REDIRECT_URI,
    scope="playlist-modify-private playlist-modify-public"
)

# Step 2: Get new access token using refresh token
token_info = oauth.refresh_access_token(SPOTIFY_REFRESH_TOKEN)
access_token = token_info["access_token"]

# Step 3: Authenticate Spotipy instance
sp = spotipy.Spotify(auth=access_token)

# Now you can use the API
user = sp.me()
print("Logged in as:", user["display_name"])