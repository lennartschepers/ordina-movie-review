from django import template
from moviereviewapp.models import Movie

register = template.Library()

@register.filter
def imdb_id_average(value):
    """ takes as argument an imdb_id, if this value exists it return the average rating of all ordina reviews"""
    movie = Movie.objects.filter(imdb_id=value).first()
    if movie.average_rating:
        return round(movie.average_rating, 1)
    else:
        return None
