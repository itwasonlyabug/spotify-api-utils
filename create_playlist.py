import sys
import utils

limit="50"
utils.get_liked_songs(limit, 'likedsongs.json')
tracklist=utils.get_track_ids('likedsongs.json')
featureList=[]
happylist=[]
sadlist=[]
feature=''

print("Getting track features...")
for each in tracklist:
    feature = utils.get_track_features(each)
    if feature['danceability'] > 0.700 and feature['valence'] > 0.500:
        featureList.append(each)
        utils.get_track_metadata(each)

utils.add_tracks_to_playlist(featureList, utils.playlist_create("PEPE"))

