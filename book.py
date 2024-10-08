import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GOOGLE_BOOKS_API_KEY")

def getBooks(recommendations):
    books = []

    for book_name in recommendations.split('\n'):
        book_name = book_name.replace(' ', '+')
        book_name = book_name[3:]

        endpoint = f"https://www.googleapis.com/books/v1/volumes?q={book_name}&key={api_key}"

        r = requests.get(endpoint)
        data = r.json()

        if not data.get('items'):
            print(f"No results found for {book_name}")
            continue

        book_info = data['items'][0]['volumeInfo']
        cover_url = book_info.get('imageLinks', {}).get('thumbnail', None)
        title = book_info.get('title', 'Unknown Title')
        description = book_info.get('description', 'No description available.')
        book_link = book_info.get('canonicalVolumeLink', None)

        if cover_url:
            cover_url = f"{cover_url}&fife=w500"
            books.append({
                'cover_url': cover_url,
                'title': title,
                'description': description,
                'link': book_link  
            })
        else:
            print(f"No cover found for this book: {book_name}")

    return books
