import spotipy
import spotipy.util as util
import lyricsgenius
import PySimpleGUI as sg
import config

# username = "SPOTIFY USERNAME"
# CLIENT_ID = "ENTER SPOTIFY CLIENT ID"
# CLIENT_SECRET = "ENTER SPOTIFY CLIENT SECRET"
# redirect_uri = "ENTER PRE-DETERMINED REDIRECT URI FROM SPOTIFY DASHBOARD"
# genius_token = "ENTER GENIUS API TOKEN"

scope = "user-read-currently-playing"

genius = lyricsgenius.Genius(config.genius_token)

token = util.prompt_for_user_token(config.username, scope, config.CLIENT_ID, config.CLIENT_SECRET, config.redirect_uri)
sp = spotipy.Spotify(auth=token)

def find_song():
	full_song = sp.current_user_playing_track()['item']
	song_name = full_song['name']

	artist_names = []
	for artist in sp.current_user_playing_track()['item']['artists']:
		artist_names.append(artist['name'])
	artist_name = artist_names[0]
	return song_name, artist_name

def find_lyrics(song, artist):
	genius_song = genius.search_song(song, artist)
	lyrics = genius_song.lyrics
	return lyrics

def has_song_changed(old_song):
	new_song = find_song()[0]
	if old_song != new_song:
		return True
	else:
		return False

current_song = ""
while True:
	song, artist = find_song()
	if song != current_song:
		print("Getting lyrics for " + song)
		current_song = song
		lyrics = find_lyrics(song, artist)
		layout = [[sg.Text(lyrics)], [sg.Button("Refresh")]]
		title = artist + ": " + song + " lyrics"
		window = sg.Window(title, layout)
		event, values = window.read(timeout = 5000)
		if event == "Refresh" or find_song()[0] != current_song:
			window.close()
			window.refresh()
			continue
		if event == sg.WIN_CLOSED:
			break


