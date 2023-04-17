import random
import dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import os


def riffle_shuffle_dict(d):
    items = list(d.items())
    random.shuffle(items)
    half = len(items) // 2
    shuffled = [items[i//2 + i % 2*half] for i in range(len(items))]
    return dict(shuffled)


def main():
    auth_manager = SpotifyOAuth(
        client_id=os.getenv('SPOTIPY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
        scope=['playlist-modify-private', 'playlist-read-private'],
        redirect_uri='http://localhost:3000'
    )
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    playlists = spotify.current_user_playlists()
    playlist_name = os.getenv('PLAYLIST_NAME').lower()

    playlist_id = next((item['id'] for item in playlists['items']
                       if item['name'].lower() == playlist_name), None)
    if not playlist_id:
        print(f"Could not find playlist '{playlist_name}'")
        return

    song_dict = {}
    playlist = spotify.playlist_items(playlist_id)
    while True:
        for idx, song in enumerate(playlist['items']):
            song_dict[song['track']['name']] = idx + len(song_dict)

        if not playlist['next']:
            break
        playlist = spotify.next(playlist)

    for _ in range(52):
        song_dict = riffle_shuffle_dict(song_dict)

    track_ids = [None] * len(song_dict)
    for idx, (song_name, pos) in enumerate(song_dict.items()):
        track_ids[idx] = spotify.search(song_name, type='track')[
            'tracks']['items'][0]['id']

    spotify.playlist_replace_items(playlist_id, track_ids)

    print("Done")


if __name__ == '__main__':
    dotenv.load_dotenv()
    main()
