import requests

TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiNmY5MzhhMWZjYjE5NmNhNDE1OTA0YzhkYTgzNjlmOCIsIm5iZiI6MTc4MDExMTcwMy42OTgsInN1YiI6IjZhMWE1OTU3ZWZiOWUzYTZhMDUzMzRjZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.MKufQBf9Rui2jOCvgZUcb6iZ-3dCZ1N5XmNa_3UKLPQ"

HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}

def obtener_populares():

    url = "https://api.themoviedb.org/3/movie/popular?language=es-MX"

    response = requests.get(
        url,
        headers=HEADERS
    )

    datos = response.json()

    return datos["results"]