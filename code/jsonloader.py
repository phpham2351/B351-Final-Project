import json
import sys
import spotipy
import spotipy.util as util
import pprint

user_id = "1239227809"
scope = 'playlist-read-private playlist-modify-private playlist-read-collaborative playlist-modify-public'
client_id = "c39874c67d6244969b9bff05d5004c90"
client_secret = "34d28707c0544ce9a9a080cb42c9b972"
token = util.prompt_for_user_token(user_id,scope, client_id = client_id, client_secret = client_secret, redirect_uri = "https://example.com/callback/")
#client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
#sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

sp = spotipy.Spotify(auth = token)

name1 = input("Song #1 Name: ") + " "
artist1 = input("Song #1 Artist: ")
name2 = input("Song #2 Name: ") + " "
artist2 = input("Song #2 Artist: ")
name3 = input("Song #3 Name: ") + " "
artist3 = input("Song #3 Artist: ")
name4 = input("Song #4 Name: ") + " "
artist4 = input("Song #4 Artist: ")
name5 = input("Song #5 Name: ") + " "
artist5 = input("Song #5 Artist: ")

name = "newSongs"

result1 = sp.search(q= name1 + artist1, limit=1)
id1 = result1['tracks']['items'][0]['id']
result2 = sp.search(q= name2 + artist2, limit=1)
id2 = result2['tracks']['items'][0]['id']
result3 = sp.search(q= name3 + artist3, limit=1)
id3 = result3['tracks']['items'][0]['id']
result4 = sp.search(q= name4 + artist4, limit=1)
id4 = result4['tracks']['items'][0]['id']
result5 = sp.search(q= name5 + artist5, limit=1)
id5 = result5['tracks']['items'][0]['id']

orig_ids = [id1, id2, id3, id4, id5]

orig_tracks = []
orig_features = []

for i in orig_ids:
    orig_tracks.append(sp.track(i))
    orig_features.append(sp.audio_features(i))

orig_data = []   

recommend = sp.recommendations(seed_tracks = orig_ids, limit = 100)

recommend_ids = []

for i in recommend['tracks']:
    recommend_ids.append(i['id'])

recommend_tracks = []
recommend_features = []

for i in recommend_ids:
    recommend_tracks.append(sp.track(i))
    recommend_features.append(sp.audio_features(i))

recommend_data = []

print("[popularity, explicit, duration, tempo, mode, danceability, energy, speechiness, loudness, acousticness, artist, name]", "\n")

print("\n", "Input data", "\n")

for i in range(0, len(orig_ids)):
    orig_data.append([orig_tracks[i]['popularity'], orig_tracks[i]['explicit'],
                 orig_features[i][0]['duration_ms'],
                 orig_features[i][0]['tempo'],
                 orig_features[i][0]['mode'],
                 orig_features[i][0]['danceability'],
                 orig_features[i][0]['energy'],
                 orig_features[i][0]['speechiness'],
                 orig_features[i][0]['loudness'],
                 orig_features[i][0]['acousticness'],
                 orig_tracks[i]['artists'][0]['name'],
                 orig_tracks[i]['name']])

for i in orig_data:
    print(i, "\n")

print("\n", "Output data", "\n")

for i in range(0, len(recommend_ids)):
    recommend_data.append([recommend_tracks[i]['popularity'], recommend_tracks[i]['explicit'],
                 recommend_features[i][0]['duration_ms'],
                 recommend_features[i][0]['tempo'],
                 recommend_features[i][0]['mode'],
                 recommend_features[i][0]['danceability'],
                 recommend_features[i][0]['energy'],
                 recommend_features[i][0]['speechiness'],
                 recommend_features[i][0]['loudness'],
                 recommend_features[i][0]['acousticness'],
                 recommend_tracks[i]['artists'][0]['name'],
                 recommend_tracks[i]['name']])

for i in recommend_data:
    print(i, "\n")
                
#playlist_id = sp.user_playlist_create(user_id, name)['id']

#sp.user_playlist_add_tracks(user_id, playlist_id, [id1, id2, id3, id4, id5])

        

                     


