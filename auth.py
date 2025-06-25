import os
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
REDIRECT_URI = os.getenv('REDIRECT_URI')

sp_oauth = SpotifyOAuth(
    client_id=SPOTIFYID,
    client_secret=SPOTIFYSECRET,
    redirect_uri=REDIRECT_URI,
    scope=["playlist-modify-private", "playlist-modify-public"],
    open_browser=True  # or False, depending on your machine
)

auth_url = sp_oauth.get_authorize_url()
print(f"Open this URL in a browser:\n{auth_url}")

# Manually paste the redirect URL after login
redirect_response = input("Paste the full redirect URL:\n")
code = sp_oauth.parse_response_code(redirect_response)

token_info = sp_oauth.get_access_token(code, as_dict=True)
print("\n✅ Copy these tokens securely:")
print("Access Token:", token_info["access_token"])
print("Refresh Token:", token_info["refresh_token"])
print("Expires In:", token_info["expires_in"])
