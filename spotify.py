import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
import re

load_dotenv()

# Spotify API credentials
CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

# Spotipy client initialization
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

def getTrackIDs(recommendations):
    track_ids = {}
    print("Recommendations:", recommendations)  # Debug line

    for line in recommendations.split('\n'):
        if line.strip():
            try:
                # Remove leading numbers and punctuation
                cleaned_line = re.sub(r'^\d+\.\s*', '', line).strip()

                parts = []

                # Check if line contains a track and artist
                if ' by ' in cleaned_line:
                    parts = cleaned_line.split(' by ')
                elif ' - ' in cleaned_line:
                    parts = cleaned_line.split(' - ')
                else:
                    # Handle artist-only recommendations
                    artist = cleaned_line.strip('\'"')
                    parts = [None, artist]

                # Check if splitting resulted in at least two parts
                if len(parts) >= 2:
                    track_name = parts[0].strip('\'"') if parts[0] else None
                    artist = parts[1].strip('\'"')

                    if track_name:
                        query = f'{track_name} by {artist}'
                    else:
                        query = f'artist:{artist}'

                    print("Query:", query)
                    result = sp.search(q=query, limit=10, type='track')

                    tracks = result.get('tracks', {}).get('items', [])
                    if tracks:
                        # Filter out tracks with terms like "karaoke", "cover", "remix"
                        filtered_tracks = [
                            track for track in tracks
                            if not any(term in track['name'].lower() for term in ["karaoke", "cover", "remix", "tribute"])
                            and track['artists'][0]['name'].lower() == artist.lower()
                        ]
                        if filtered_tracks:
                            # Further prioritize tracks that are part of an official album by the artist
                            official_tracks = [
                                track for track in filtered_tracks
                                if any(artist.lower() in alb_artist['name'].lower() for alb_artist in track['album']['artists'])
                            ]
                            chosen_track = official_tracks[0] if official_tracks else filtered_tracks[0]
                            track_id = chosen_track['id']
                            track_ids[line.strip()] = track_id
                            print("Track ID:", track_id)  # Debug line
                        else:
                            # If no filtered tracks are found, just add the first track from the search results
                            track_id = tracks[0]['id']
                            track_ids[line.strip()] = track_id
                            print(f"No original tracks found for query: {query}. Added first search result.")
                    else:
                        print(f"No tracks found for query: {query}")
                else:
                    print(f"Invalid split result: {parts}")
            except IndexError as e:
                print(f"Error due to format issue: {line} - {e}")
            except Exception as e:
                print(f"Unexpected error: {line} - {e}")

    return track_ids
