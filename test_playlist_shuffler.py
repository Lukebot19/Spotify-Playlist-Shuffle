import random
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from tkinter import messagebox

from main import main, riffle_shuffle_dict, shuffle_playlist
import flake8

def test_riffle_shuffle_dict():
    # Test if the riffle_shuffle_dict function shuffles a dictionary correctly
    d = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}
    shuffled_d = riffle_shuffle_dict(d)
    assert set(d.keys()) == set(shuffled_d.keys())
    assert set(d.values()) == set(shuffled_d.values())
    assert d != shuffled_d


def test_shuffle_playlist():
    # Test if the shuffle_playlist function shuffles a playlist correctly
    spotify = SpotifyClientCredentials()
    playlist_listbox = None
    shuffle_playlist(spotify, playlist_listbox)
    assert messagebox.showerror.called
    assert messagebox.showinfo.called


def test_main():
    # Test if the main function runs without any errors
    main()


def test_flake8():
    # Test if the code passes Flake8's linting checks
    flake8style = flake8.get_style_guide()
    result = flake8style.check_files(['playlist_shuffler.py'])
    assert result.total_errors == 0
