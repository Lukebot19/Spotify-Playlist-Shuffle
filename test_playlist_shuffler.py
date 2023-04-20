import random
from tkinter import messagebox

from main import main, riffle_shuffle_dict, shuffle_playlist
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import os
import dotenv

def test_riffle_shuffle_dict():
    # Test if the riffle_shuffle_dict function shuffles a dictionary correctly
    d = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}

    for _ in range(52):
        shuffled_d = riffle_shuffle_dict(d)
    
    assert set(d.keys()) == set(shuffled_d.keys())
    assert set(d.values()) == set(shuffled_d.values())
    assert str(shuffled_d) != str(d)


def test_shuffle_playlist():
    # Test if the shuffle_playlist function shuffles a playlist correctly
    dotenv.load_dotenv()
    spotify = spotipy.Spotify(
        client_credentials_manager=SpotifyOAuth(
            client_id=os.getenv('SPOTIPY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
            scope=['playlist-modify-private', 'playlist-read-private'],
            redirect_uri='http://localhost:3000'
        )
    )
    playlist_listbox = None
    shuffle_playlist(spotify, playlist_listbox)


def test_main():
    # Test if the main function runs without any errors
    main()
