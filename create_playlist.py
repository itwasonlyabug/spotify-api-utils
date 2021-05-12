import utils
from secrets import user_id, spotify_ready_token

cmd = utils.commandline_menu()

danceability=cmd.get('TRACK_DANCE')
valence=cmd.get('TRACK_VALENCE')
playlist_name=cmd.get('PLAYLIST_NAME')
limit=cmd.get('REQUEST_LIMIT')
offset=50

featureList=[]
happylist=[]
sadlist=[]
feature=''

playlist=utils.playlist_create(playlist_name, user_id)
liked_songs=utils.get_liked_songs(limit, 'likedsongs.json')
tracklist=utils.track_get_ids('likedsongs.json')

for each in tracklist:
    feature = utils.track_get_features(each)
    if feature['danceability'] > danceability and feature['valence'] > valence:
        featureList.append(each)
        #utils.track_get_metadata(each)

utils.add_tracks_to_playlist(featureList, playlist)
