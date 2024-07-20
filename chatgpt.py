import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY')
)

def getRecomendations(media, content):
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are to give me media recommendations in a list with no extra text."},
      {"role": "user", "content": f'Give me {media} recommendations based on {content}'},
    ]
  )

  recommendations = completion.choices[0].message.content
  return recommendations
