# Playlist Shuffler

Playlist Shuffler is a Python program that shuffles the songs in a user's Spotify playlist using a riffle shuffle algorithm. The program uses the Spotify Web API to access a user's playlists and modify them. 

## Requirements

To run the program, you will need to have Python 3 installed. You will also need to create a Spotify app in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) to obtain your client ID and client secret. You will also need to set the redirect URI in the Spotify app settings to "http://localhost:3000". 

## Installation

1. Clone the repository onto your local machine.
2. Navigate to the project directory.
3. Install the required packages by running `pip install -r requirements.txt`.
4. Create a `.env` file in the project directory and add the following lines, replacing `YOUR_CLIENT_ID` and `YOUR_CLIENT_SECRET` with your actual client ID and client secret:

```
SPOTIPY_CLIENT_ID=YOUR_CLIENT_ID
SPOTIPY_CLIENT_SECRET=YOUR_CLIENT_SECRET
```


## Usage

To run the program, open a terminal in the project directory and run the command `python playlist_shuffler.py`. 

Once the program is running, you will see a window with a list of your Spotify playlists. Select a playlist from the list and click the "Shuffle" button to shuffle the songs in the playlist. 

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.


## Credits
Playlist Shuffler was created by Luke Alexander. It utilizes the Spotipy library by Paul Lamere.