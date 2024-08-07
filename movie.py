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

        #Updated to include name, description, and trailer
        movie_data = data['results'][0]
        movie_id = movie_data['id']
        movie_title = movie_data['title']
        movie_description = movie_data['overview']

        # TMDB movie page link
        tmdb_link = f"https://www.themoviedb.org/movie/{movie_id}"

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
        trailers.append({
            'title': movie_title,
            'description': movie_description,
            'trailer_url': yt_url,
            'tmdb_link': tmdb_link
        })

    return(trailers)
