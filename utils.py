'''Functions that allow Spotify playlist and track manipulation'''
from secrets import user_id, spotify_ready_token
import json
import re
import os
import logging
import requests

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
    encoding='utf-8',
    level=logging.INFO)

SPOTIFY_API_URL = 'https://api.spotify.com/v1/'
USERS_API = SPOTIFY_API_URL+'users/'
PLAYLIST_API = USERS_API+user_id+'/playlists'
PLAYLIST_TRACK_API = SPOTIFY_API_URL+'playlists/'
TRACK_API = SPOTIFY_API_URL+'tracks/'
AUDIO_FEATURES = SPOTIFY_API_URL+'audio-features/'

headers={
            "Content-Type": "application/json",
            "Authorization" : "Bearer {}".format(spotify_ready_token)}

def json_to_file(filename, json_data):
    '''Saves json_data contents to filename file'''
    with open(filename, 'w') as json_file:
        json.dump(json_data, json_file)
        logging.info('File created: %s', filename)
        logging.debug('%s', json_data)
    return filename

def track_get_metadata(track_id):
    '''Gets Metadata (album name, artist and etc.) of song'''
    #logging.info("Getting track metadata...")
    track_general = requests.get((TRACK_API + track_id), headers=headers).json()
    track_artist = track_general['artists'][0]['name']
    track_name = track_general['name']
    track_album_name = track_general['album']['name']
    track_metadata = track_artist + ' - ' + track_name + ' / ' + track_album_name
    logging.debug('Getting metadata for: %s : %s', track_id, track_general)
    return track_metadata

def track_get_features(track_id):
    '''Gets Audio features of track (valence, danceability and etc)'''
    url = AUDIO_FEATURES + track_id
    track_features = requests.get(url, headers=headers).json()
    logging.debug('Getting track features for: %s : %s', track_id, track_features)
    return track_features

def track_get_ids(filename):
    '''Gets all track IDs from a file'''
    track_ids=[]
    data = {}
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
        for each in range (0, len(data['items'])):
            track_ids.append(data['items'][each]['track']['id'])
    logging.debug('Getting track ids from: %s', filename)
    logging.debug('%s', track_ids)
    return track_ids

def get_liked_songs(spotify_limit, filename):
    '''Get songs from the user's Liked Songs'''
    # To prevent spam of Spotify's servers, I save the Library list to a file
    # before continuing
    if os.path.exists(filename):
        logging.info('Songs file - %s found', filename)
    else:
        requests.post((USERS_API+user_id), headers=headers)
        library_list = requests.get((SPOTIFY_API_URL + 'me/tracks?limit='+spotify_limit),
                headers=headers)
        if (re.search(r'\[2[0-9][0-9]\]', str(library_list))) is True:
            logging.error('Error Code: %s', library_list)
            return 1
        else:
            json_to_file(filename, library_list.json())
            liked_songs = library_list.json()
            logging.info('Got songs: %s', liked_songs)
            return liked_songs
    return filename

def playlist_exists(name):
    '''Check if a Playlist with this name already exists'''
    response = requests.get("https://api.spotify.com/v1/users/"+user_id+"/playlists?limit=50",
            headers=headers)
    if re.search(name, str(response.json())) is True:
        logging.debug(response.json())
        logging.info('Playlist %s already exists', name)
        return True
    logging.debug('%s', response.json())
    return False

def playlist_has_track(playlist_id, track_id):
    '''Check if a Playlist already contains this track'''
    response = requests.get("https://api.spotify.com/v1/playlists/"+playlist_id+"/tracks?limit=50",
            headers=headers)
    if re.search(track_id, str(response.json())) is True:
        logging.debug(response.json())
        logging.info('Playlist already contains track: %s', track_id)
        return True
    return False

def playlist_create(name):
    '''Create new Playlist for the current user'''
    if playlist_exists(name) is True:
        return 1
    else:
        requests.post((USERS_API+user_id), headers=headers)

        request_body=json.dumps({
            "name": name,
            "public": True})

        response = requests.post(PLAYLIST_API, headers=headers, data=request_body)
        playlist_id = response.json()['id']
        logging.info('Playlist %s created.',name)
        return playlist_id

def add_tracks_to_playlist(track_ids, playlist_id):
    '''Adds track(s) to a specific Playlist'''
    logging.info("Adding songs to playlist...")
    new_tracks=[]
    for each in track_ids:
        if playlist_has_track(playlist_id, each) is True:
            pass
        else:
            new_tracks.append(each)

    new_tracks_uris = ['spotify:track:' + x for x in new_tracks]
    track_uris = ','.join(new_tracks_uris)
    response = requests.post("https://api.spotify.com/v1/playlists/"+
        playlist_id+"/tracks?uris="+track_uris,
        headers=headers)

    logging.info('Tracks added: %s to Playlist: %s', track_uris, playlist_id)
    return response
