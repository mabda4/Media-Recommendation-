import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("TMBD_API_KEY")

def getTrailers(recommendations):
    trailers = []
    print(recommendations)
    for movie_name in recommendations.split('\n'):
        movie_name = movie_name.replace(' ', '+')
        movie_name = movie_name[3:]
        
        endpoint = f"https://api.themoviedb.org/3/search/movie?query={movie_name}&api_key={api_key}"
        

        r = requests.get(endpoint)
        data = r.json()

        if not data['results']:
            print(f"No results found for {movie_name}")
            continue

        movie_id = data['results'][0]['id']

        endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={api_key}"

        r = requests.get(endpoint)
        data = r.json()

        trailer_id = None

        for result in data['results']:
            if result['type'] == 'Trailer':
                trailer_id = result['key']
                break

        if trailer_id is None:
            continue

        yt_url = f"https://www.youtube.com/embed/{trailer_id}"
        trailers.append(yt_url)

    return(trailers)

