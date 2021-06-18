import os
import unittest
import json
import utils

class TestFileOperations(unittest.TestCase):
    TESTFILE = 'testfile.json'
    def test_write(self):
        '''Creates file and writes to it, then deletes it'''
        file = utils.json_to_file(TestFileOperations.TESTFILE, '{"test": "success"}')
        self.assertEqual(file, TestFileOperations.TESTFILE)
        os.remove(TestFileOperations.TESTFILE)
        self.assertFalse(os.path.isfile('./'+TestFileOperations.TESTFILE))

class TestTrackOperations(unittest.TestCase):
    SAMPLE_TRACK_ID = '34wcz4mpAActEc6gtqX3wz'
    TESTFILE = 'test_likedsong.json'
    def test_features(self):
        features = utils.track_get_features(TestTrackOperations.SAMPLE_TRACK_ID)
        danceability = features.get('danceability')
        self.assertEqual(danceability, float('0.674'))

    def test_metadata(self):
        metadata = utils.track_get_metadata(TestTrackOperations.SAMPLE_TRACK_ID)
        self.assertIn('Jungle', metadata)
    
    def test_liked_song(self):
        liked_song = utils.get_liked_songs('1', TestTrackOperations.TESTFILE)
        self.assertTrue(os.path.isfile('./'+liked_song))
        with open(liked_song, 'r') as file:
            data = file.read()
            self.assertIn('spotify', str(data))

class TestPlaylistOperations(unittest.TestCase):
    def test_getting_playlists(self):
        get_all_playlists(filename, userid)

if __name__ == '__main__':
    unittest.main()
