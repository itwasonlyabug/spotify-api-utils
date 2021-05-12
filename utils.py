'''Functions that allow Spotify playlist and track manipulation'''
from secrets import user_id, spotify_ready_token
import json
import re
import os
import logging
import argparse
import requests


# Logging settings
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
    encoding='utf-8',
    level=logging.INFO)

# Hardcoded URLs
SPOTIFY_API_URL = 'https://api.spotify.com/v1/'
USERS_API = SPOTIFY_API_URL+'users/'
USER_ID_API = USERS_API+user_id
PLAYLIST_API = USERS_API+user_id+'/playlists'
PLAYLIST_TRACK_API = SPOTIFY_API_URL+'playlists/'
TRACK_API = SPOTIFY_API_URL+'tracks/'
AUDIO_FEATURES = SPOTIFY_API_URL+'audio-features/'

# General Headers
headers={
            "Content-Type": "application/json",
            "Authorization" : "Bearer {}".format(spotify_ready_token)}

def commandline_menu():
    '''Handles commandline arguments'''
    #WIP, not implemented
    parser = argparse.ArgumentParser(description='Create custom playlists via Spotify\'s API')
    parser.add_argument('-p', '--playlist',
        dest='PLAYLIST_NAME',
        type=str,
        required=True,
        help='name of playlist to be created')
    parser.add_argument('-l', '--limit',
        dest='REQUEST_LIMIT',
        type=str,
        help='limit of objects to pull with each api call (min 0, max 50)',
        default=50)
    parser.add_argument('-v', '--valence',
        dest='TRACK_VALENCE', 
        type=float,
        metavar="[0.000-1.000]",
        help='sets desired valence of the tracks')
    parser.add_argument('-d', '--danceability',
        dest='TRACK_DANCE', 
        type=float,
        metavar="[0.000-1.000]",
        help='sets desired danceability of the tracks')
    args = parser.parse_args()
    return vars(args)

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

        json_to_file(filename, library_list.json())
        liked_songs = library_list.json()
        logging.info('Got songs: %s', liked_songs)
        return liked_songs
    return filename

def get_all_playlists(filename, userid):
    '''Get all playlists of selected user'''
    requests.post(('https://api.spotify.com/v1/users/'+userid), headers=headers)
    offset=0
    items=1
    playlists = []
    while items != 0:
        response = requests.get(
            "https://api.spotify.com/v1/users/"+userid+"/playlists?limit=50&offset="+str(offset),
            headers=headers).json()
        offset=offset+50
        items = len(response['items'])
        playlists.append([i['name'] for i in response['items']])
    logging.info('Got playlists...')
    logging.debug('Got playlists: %s', playlists)
    json_to_file(filename, playlists)
    return playlists

def playlist_exists(name, userid):
    '''Check if a Playlist with this name already exists'''
    playlists = str(get_all_playlists('playlists.json', userid))
    logging.debug('%s', playlists)

    if re.search(name, playlists):
        logging.info('Playlist %s already exists', name)
        return True
    return False

def playlist_get_tracks(playlist_id):
    '''Get all tracks from the selected playlist'''
    offset=0
    items=1
    playlist_tracks = []
    playlist_tracks_names = []
    while items != 0:
        response = requests.get(
            PLAYLIST_TRACK_API+playlist_id+"/tracks?limit=50&offset="+str(offset),
            headers=headers).json()
        logging.debug('Response: %s', response)
        offset=offset+50
        items = len(response['items'])
        playlist_tracks.append([i['track']['id'] for i in response['items']])
        playlist_tracks_names.append([i['track']['name'] for i in response['items']])
    logging.info('Got tracks: %s', playlist_tracks_names)
    logging.debug('Got tracks: %s', playlist_tracks)
    return playlist_tracks

def playlist_create(name, userid):
    '''Create new Playlist for the current user'''
    if playlist_exists(name, userid) is False:
        requests.post((USERS_API+user_id), headers=headers)

        request_body=json.dumps({
            "name": name,
            "public": True})

        response = requests.post(PLAYLIST_API, headers=headers, data=request_body)
        playlist_id = response.json()['id']
        logging.info('Playlist %s created.',name)
        return playlist_id
    return 1

def add_tracks_to_playlist(track_ids, playlist_id):
    '''Adds track(s) to the selected Playlist'''
    logging.info("Adding songs to playlist %s ...", playlist_id)
    tracks = playlist_get_tracks(playlist_id)
    new_tracks = []
    for each in enumerate(track_ids):
        if track_ids[each] in tracks:
            logging.info('Playlist already contains track: %s', track_ids[each])
        else:
            logging.info('Adding track %s to playlist...', track_ids[each])
            new_tracks.append(track_ids[each])

    new_tracks_uris = ['spotify:track:' + x for x in new_tracks]
    track_uris = ','.join(new_tracks_uris)
    response = requests.post(PLAYLIST_TRACK_API+
        playlist_id+"/tracks?uris="+track_uris,
        headers=headers)

    logging.info('Tracks added: %s to Playlist: %s', track_uris, playlist_id)
    return response
