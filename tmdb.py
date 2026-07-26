import requests

TOKEN = "TU_BEARER_TOKEN"

HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}

def obtener_populares():
    url = "https://api.themoviedb.org/3/movie/popular?language=es-MX"

    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()["results"]

    return []


def obtener_por_genero(genero):
    url = (
        f"https://api.themoviedb.org/3/discover/movie"
        f"?language=es-MX"
        f"&with_genres={genero}"
    )

    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()["results"]

    return []