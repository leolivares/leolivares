from datetime import datetime as dt
from functools import reduce



def set_id():
    i = 0
    while True :
        yield id
        i += 1


class Cast:
    def __init__(self, movie_title, name, character):
        self.name = name
        self.movie = movie_title
        self.character = character


class Movie:
    get_id = set_id()

    def __init__(self, title, rating, release, *args):
        self.id = next(Movie.get_id)
        self.title = title
        self.rating = float(rating)
        self.release = dt.strptime(release, '%Y-%m-%d')  # 2015-03-04
        self.genres = list(args)

def popular(num):
    return filter(lambda x: x.rating >= num, movies)

def with_genres(num):
    return filter(lambda x: len(x.genres) >= num, movies)

def top_of_genre(genero):
    one_genre = sorted(list(filter(lambda x: genero in x.genres, movies)), key= lambda x: x.rating, reverse=True)
    return one_genre[:10]

def actor_rating(nombre):
    peliculas = list(c.movie for c in filter(lambda x: x.name == nombre, cast))

    if len(peliculas) > 0 :
        return reduce(lambda x,y: x+y,map(lambda x: x.rating,filter(lambda x: x.title in peliculas , movies))) / len(peliculas)

def compare_actors(nombre1,nombre2):
    rating1 = actor_rating(nombre1)
    rating2 = actor_rating(nombre2)
    print(rating1,rating2)
    return nombre1 if rating1 > rating2 else nombre2

def movies_of(nombre):
    return [tuple([c.movie , c.character]) for c in filter(lambda x: x.name == nombre, cast)]




if __name__ == "__main__":

    parser = lambda line: line.strip().split(",")

    with open('movies2.txt', 'r') as f:
        movies = [Movie(*mov.strip().split(",")[1:]) for mov in f]

    with open('cast2.txt', 'r') as f:
        cast = [Cast(*parser(line)) for line in f]

    lista = list(popular(3))
    print(lista)

    lista2 = list(with_genres(6))
    print(lista2[0].title)

    lista3 = top_of_genre("Drama")
    print(lista3)

    print(actor_rating("Natalie Portman"))

    compare_actors("Natalie Portman","Mila Kunis")

    print(movies_of("Natalie Portman"))



