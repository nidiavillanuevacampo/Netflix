from tmdb import obtener_populares

peliculas = obtener_populares()

print(peliculas[0]["title"])