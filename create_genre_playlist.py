import utils as utils
from secrets import spotify_token, spotify_user_id, user_id, spotify_ready_token


limit = '50'

utils.getLikedSongs(limit, 'likedsongs.json')
tracklist=utils.getTrackIds('likedsongs.json')
featureList=[]
happylist=[]
sadlist=[]
feature=''

for each in tracklist:
    feature = utils.getTrackFeatures(each)
    if feature['danceability'] > 0.700 and feature['valence'] > 0.500:
        featureList.append(each)
        utils.getTrackMetadata(each)

string = 'spotify:track:'
song_list = [string + x for x in featureList]
songs = ','.join(song_list)
print(utils.addTrackToPlaylist(songs, "0JITFS3sKzsqNJ4g6W4QqM"))
