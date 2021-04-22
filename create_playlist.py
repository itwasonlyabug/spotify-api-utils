import sys,re
import utils

limit = '3'

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

print("Adding song(s) to playlist...")
utils.add_tracks_to_playlist(tracklist, "0JITFS3sKzsqNJ4g6W4QqM")

