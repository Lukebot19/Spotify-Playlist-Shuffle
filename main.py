import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import dotenv
import os
from tkinter import *
from tkinter import messagebox  # import messagebox function from tkinter



def main():
    spotify = spotipy.Spotify(
        client_credentials_manager=SpotifyOAuth(
            client_id=os.getenv('SPOTIPY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
            scope=['playlist-modify-private', 'playlist-read-private'],
            redirect_uri='http://localhost:3000'
        )
    )

    window = Tk()
    window.title("Playlist Shuffler")

    # Create and add widgets to the window
    title_label = Label(window, text="Choose a playlist to shuffle:")
    title_label.pack()

    playlist_listbox = Listbox(window, height=10, width=50)
    playlist_listbox.pack()

    shuffle_button = Button(window, text="Shuffle", command=lambda: shuffle_playlist(
        spotify, playlist_listbox))
    shuffle_button.pack()

    # Populate the playlist Listbox with the user's playlists
    playlists = spotify.current_user_playlists()
    for item in playlists['items']:
        playlist_listbox.insert(END, item['name'])

    window.mainloop()


def shuffle_playlist(spotify, playlist_listbox):

    selection = playlist_listbox.curselection()
    if len(selection) == 0:
        messagebox.showerror("Error", "Please select a playlist to shuffle.")
        return

    # Get the ID of the selected playlist
    playlist_idx = spotify.current_user_playlists()[
        'items'][selection[0]]['id']

    song_dict = {}

    playlist = spotify.playlist_items(playlist_id=playlist_idx)
    num = playlist['total']

    my_count = 0

    while num > 0:

        for idx, song in enumerate(playlist['items']):
            song_dict[song['track']['name']] = idx + my_count

        num -= 100
        my_count += 100

        playlist = spotify.playlist_items(
            playlist_id=playlist_idx, offset=my_count)

    for _ in range(52):
        song_dict = riffle_shuffle_dict(song_dict)

    for itemidx, item in enumerate(song_dict):
        spotify.playlist_reorder_items(
            playlist_id=playlist_idx, range_start=song_dict[item], range_length=1, insert_before=itemidx)

    messagebox.showinfo("Success", "Playlist shuffled successfully.")


def riffle_shuffle_dict(d):
    items = list(d.items())
    random.shuffle(items)
    half = len(items) // 2
    shuffled = []
    for i in range(half):
        shuffled.append(items[i])
        shuffled.append(items[i+half])
    if len(items) % 2 == 1:
        shuffled.append(items[-1])
    return dict(shuffled)


if __name__ == '__main__':
    dotenv.load_dotenv()
    main()
