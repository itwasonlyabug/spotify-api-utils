import json, re, os
import requests
from secrets import spotify_token, spotify_user_id, user_id, spotify_ready_token

spotify_api_url = 'https://api.spotify.com/v1/'
users_api = spotify_api_url+'users/'
playlist_api = users_api+user_id+'/playlists'
playlist_track_api = spotify_api_url+'playlists/'
track_api = spotify_api_url+'tracks/'
audio_features = spotify_api_url+'audio-features/'


headers={
      "Content-Type": "application/json",
      "Authorization" : "Bearer {}".format(spotify_ready_token)}
data = {}

def getTrackMetadata(track_id):
  
  track_general = requests.get((track_api + track_id), headers=headers).json()
  track_artist = track_general['artists'][0]['name']
  track_name = track_general['name']
  track_album_name = track_general['album']['name']
  track_metadata = track_artist + ' - ' + track_name + ' / ' + track_album_name

  return track_metadata

def getTrackFeatures(track_id):
  url = audio_features + track_id
  track_features = requests.get(url, headers=headers).json()
  return track_features

def getLikedSongs(spotify_limit, filename):
    # To prevent spam of Spotify's servers, I save the Library list to a file
    # before continuing
    if os.path.exists(filename):
        return filename
    else:
      requests.post((users_api+user_id), headers=headers)
      library_list = requests.get((spotify_api_url + 'me/tracks?limit='+spotify_limit), headers=headers)
      if (re.search(r'\[2[0-9][0-9]\]', str(library_list))) == True:
        print("Error Code: ", library_list)
        return 1
      else:
        jsonToFile(filename, library_list.json())
 
        return library_list.json()

def jsonToFile(filename, json_data):
    with open(filename, 'w') as json_file:
        json.dump(json_data, json_file)
    return ("File created: ", filename)

def createPlaylist(name):
  requests.post((users_api+user_id), headers=headers)

  request_body=json.dumps({
      "name": name,
      "public": True})
  
  response = requests.post(playlist_api, headers=headers, data=request_body)
  playlist_id = response.json()['id'] 

  return playlist_id

def addTrackToPlaylist(track_uris, playlist_id):
    action = requests.post((users_api+user_id), headers=headers)
    response = requests.post(playlist_track_api+playlist_id+"/tracks?uris="+track_uris)
    print(playlist_track_api+playlist_id+"/tracks?uris="+track_uris)
    return response

def getTrackIds(filename):
    tracks=[]
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
        for each in range (0, len(data['items'])):
            tracks.append(data['items'][each]['track']['id'])

    return tracks
