import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import dotenv
import os


def main():
    spotify = spotipy.Spotify(
        client_credentials_manager=SpotifyOAuth(
            client_id=os.getenv('SPOTIPY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
            scope=['playlist-modify-private', 'playlist-read-private'],
            redirect_uri='http://localhost:3000'
        )
    )

    playlists = spotify.current_user_playlists()

    # Prompt the user to select a playlist to shuffle
    print("Choose a playlist to shuffle:")
    for idx, item in enumerate(playlists['items']):
        print(f"{idx+1}. {item['name']}")
    selection = int(input("Enter the number of the playlist: "))

    # Get the ID of the selected playlist
    playlist_idx = playlists['items'][selection-1]['id']

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

    print("Done")


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
