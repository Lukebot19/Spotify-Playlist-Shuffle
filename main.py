import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import dotenv
import os
import tkinter as tk


def main():
    # create Spotify client
    spotify = spotipy.Spotify(
        client_credentials_manager=SpotifyOAuth(
            client_id=os.getenv('SPOTIPY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
            scope=['playlist-modify-private', 'playlist-read-private'],
            redirect_uri='http://localhost:3000'
        )
    )

    # get user's playlists
    playlists = spotify.current_user_playlists()

    # create GUI
    root = tk.Tk()
    root.title("Spotify Playlist Shuffler")

    # add label
    label = tk.Label(root, text="Choose a playlist:")
    label.pack()

    # add listbox
    listbox = tk.Listbox(root, selectmode="single")
    listbox.pack()

    # add playlist names to listbox
    for playlist in playlists["items"]:
        listbox.insert(tk.END, playlist["name"])

    # add button
    button = tk.Button(root, text="Shuffle Playlist", command=lambda: shuffle_playlist(
        listbox.get(listbox.curselection()), spotify))
    button.pack()

    root.mainloop()


def shuffle_playlist(playlist_name, spotify):
    # get user's playlists
    playlists = spotify.current_user_playlists()

    # find the playlist with the matching name
    for playlist in playlists["items"]:
        if playlist["name"] == playlist_name:
            playlist_id = playlist["id"]
            break

    # get all songs in the playlist
    songs = []
    results = spotify.playlist_items(
        playlist_id, fields="items(track(name, id)), next", additional_types=['track'])
    while results:
        for song in results["items"]:
            songs.append(song["track"]["id"])
        if results["next"]:
            results = spotify.next(results)
        else:
            break

    # shuffle the list of song IDs
    for _ in range(52):
        songs = riffle_shuffle_list(songs)

    # replace the playlist with the shuffled songs
    spotify.playlist_replace_items(playlist_id, songs)

    print(f"Playlist '{playlist_name}' has been shuffled!")


def riffle_shuffle_list(lst):
    half = len(lst) // 2
    left, right = lst[:half], lst[half:]
    shuffled = []
    for i in range(half):
        shuffled.append(left[i])
        shuffled.append(right[i])
    if len(lst) % 2 == 1:
        shuffled.append(lst[-1])
    return shuffled


if __name__ == '__main__':
    dotenv.load_dotenv()
    main()
