def get_id():
    i = 0
    while True:
        yield i
        i += 1


class Movie:
    id = get_id()

    def __init__(self, _, title, rating, release, *genres):
        self.id = next(Movie.id)
        self.title = title
        self.rating = float(rating)
        self.release = release
        self.genres = list(genres)


class Cast:

    def __init__(self, *args):
        pass

parser = lambda line: line.rstrip("\n").split(",")

MOVIES = list()
with open("movies.txt") as file:
    MOVIES = [Movie(*parser(line)) for line in file]

CASTS = list()
with open("cast.txt") as file:
    CASTS = [Cast(*parser(line)) for line in file]


def popular(movies, n):
    """ Retorna una lista de peliculas con rating sobre n"""
    return filter(lambda x: x.rating >= n, movies)

for top in popular(MOVIES, 20):
    print(top.title)


def with_genres(movies, n):
    """Retorna una lista de peliculas con mas de n generos """
    return filter(lambda x: len(x.genres) >= n, movies)


def tops_of_genre(movies, genre):
    """ Retorna las 10 mejores peliculas de un género"""
    one_genre = sorted(filter(lambda x: genre in x.genres, movies),key = lambda x: x.rating)

    return one_genre[:10] if len(one_genre) > 10 else one_genre


for i, top in enumerate(tops_of_genre(MOVIES, "Drama")):
    print(i + 1, top.title)

from functools import reduce


def actor_rating(movies, casts, actor):
    """Dado el nombre de un actor, retorna el promedio del rating de las
        peliculas en las que ha participado """

    actor_movies = [c.movie for c in filter(lambda cast: cast.name == actor, casts)]

    if len(actor_movies) > 0:
        return reduce(lambda x, y: x+y, map(lambda m: m.rating, filter(lambda movie: movie.title in actor_movies,
                                                                       movies))) / len(actor_movies)

