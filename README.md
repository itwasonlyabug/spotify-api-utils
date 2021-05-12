## Known Issues

* Commandline arguments do not work correctly yet (you will get an error)

## Usage

1. Create a file called 'secrets.py'.

   ```python
     spotify_ready_token = 'reallylongstringwithlotsofstuff'
     userid = 'yourusername'
   ```

2. Add your Spotify userid and token to the `secrets.py`.
3. [optional] Edit `create_playlist.py` and change the `for` loop to change the parameters.
4. Run `python3 create_playlist.py --help`.
