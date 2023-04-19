import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import dotenv
import os
from tkinter import *
from tkinter import messagebox  # import messagebox function from tkinter



def main():
    """
    Create the main window and widgets for the playlist shuffler.
    """

    # Spotify authentication and authorization
    spotify = spotipy.Spotify(
        client_credentials_manager=SpotifyOAuth(
            client_id=os.getenv('SPOTIPY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
            scope=['playlist-modify-private', 'playlist-read-private'],
            redirect_uri='http://localhost:3000'
        )
    )

    # Create the main window
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

    # Run the main window loop
    window.mainloop()


def shuffle_playlist(spotify, playlist_listbox):
    """
    Shuffle the selected Spotify playlist.

    Parameters:
    spotify (spotipy.Spotify): The authenticated Spotify API client.
    playlist_listbox (tkinter.Listbox): The tkinter Listbox containing the user's playlists.

    Returns:
    None.
    """

    # Check if a playlist is selected
    selection = playlist_listbox.curselection()
    if len(selection) == 0:
        messagebox.showerror("Error", "Please select a playlist to shuffle.")
        return

    # Get the ID of the selected playlist
    playlist_idx = spotify.current_user_playlists()[
        'items'][selection[0]]['id']

    song_dict = {}

    # Get all the songs in the playlist
    playlist = spotify.playlist_items(playlist_id=playlist_idx)
    num = playlist['total']

    my_count = 0

    # Build a dictionary of song names and their corresponding index in the playlist
    while num > 0:

        for idx, song in enumerate(playlist['items']):
            song_dict[song['track']['name']] = idx + my_count

        num -= 100
        my_count += 100

        playlist = spotify.playlist_items(
            playlist_id=playlist_idx, offset=my_count)

    # Shuffle the song dictionary 52 times using a riffle shuffle algorithm
    for _ in range(52):
        song_dict = riffle_shuffle_dict(song_dict)

    # Reorder the playlist based on the shuffled song dictionary
    for itemidx, item in enumerate(song_dict):
        spotify.playlist_reorder_items(
            playlist_id=playlist_idx, range_start=song_dict[item], range_length=1, insert_before=itemidx)

    # Show success message
    messagebox.showinfo("Success", "Playlist shuffled successfully.")


def riffle_shuffle_dict(d):
    """
    Shuffle a dictionary using a riffle shuffle algorithm.

    Parameters:
    d (dict): The dictionary to be shuffled.

    Returns:
    dict: The shuffled dictionary.
    """
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
