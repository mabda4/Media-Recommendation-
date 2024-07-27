from requests import post
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("TWITCH_CLIENT_ID")
secret = os.environ.get("TWITCH_CLIENT_SECRET")
response = post(f"https://id.twitch.tv/oauth2/token?client_id={api_key}&client_secret={secret}&grant_type=client_credentials")
access_token = "Bearer " + response.json()['access_token']

def getPictures(recommendations):
    print(recommendations)
    pictures = {}
    for gameName in recommendations.split('\n'):
        album = []
        gameName = gameName[3:]

        game_data_response = post(
            'https://api.igdb.com/v4/games',
            headers={
                'Client-ID': api_key,
                'Authorization': access_token
            },
            data=f'fields artworks; search "{gameName}";'
        )

        game_data = game_data_response.json()

        if not game_data:
            continue

        for game in game_data:
            gameId = game['id']
            imglink_response = post(
                'https://api.igdb.com/v4/artworks',
                headers={
                    'Client-ID': api_key,
                    'Authorization': access_token
                },
                data=f'fields url; where game = {gameId};'
            )
            artwork_data = imglink_response.json()
            print(artwork_data)

            if not artwork_data:
                continue

            for artwork in artwork_data:
                url = artwork['url']
                url = url.replace("t_thumb", "t_original")
                album.append(f"https:{url}")

        pictures[gameName] = album

    return pictures


