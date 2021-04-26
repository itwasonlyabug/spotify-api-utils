## Known Issues

* Playlist creation does not check if a playlist with the same name already exists. Spotify allows you to have unlimited(?) playists with the same name.
* Adding tracks to an existing playlist does not check if those tracks are already in the playlist.
* Commandline arguments do not work yet.

## Usage

1. Create a file called 'secrets.py'.

   ```python
     spotify_ready_token = 'reallylongstringwithlotsofstuff'
     userid = 'yourusername'
   ```

2. Add your Spotify userid and token to the `secrets.py`.
3. [optional] Edit `create_playlist.py` and change the `for` loop to change the parameters.
4. Run `python3 create_playlist.py`.
