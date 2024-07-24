import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

load_dotenv()

# Spotify API credentials
CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

# Spotipy client initialization
sp =spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

#Get Track IDs from the list of recommendation
def getTrackIDs(recommendations):
    track_ids = {}
    print("Recommendations", recommendations) #debug line

    for line in recommendations.split('\n'):
        if line.strip():
            try:
                # If-statements for where to split the string. Sometimes the format is different
                #example, there's "track name by artist" or "track name - artist"
                if ' by ' in line:
                    parts = line.split(' by ')
                elif ' - ' in line:
                    parts = line.split(' - ')
            
                track_name = parts[0].strip().strip('"')
                artist = parts[1].strip().strip('"')
                
                query = f'{track_name} by {artist}'
                #debug query
                print("Query", query)
                result = sp.search(q=query, limit=1, type='track')
                
                tracks = result.get('tracks', {}).get('items', [])
                if tracks:
                    track_id = tracks[0]['id']
                    track_ids[line.strip()] = track_id
                    print("Track ID:", track_id) #debug line
            except IndexError:
                print(f"Error due to format issue: {line}")

    return track_ids

