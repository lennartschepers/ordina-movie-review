from django import template
from moviereviewapp.models import Movie

register = template.Library()

@register.filter
def imdb_to_ordina_id(value):
    """ takes as argument an imdb_id, if this value exists it will return the corresponding normal id"""
    movie = Movie.objects.filter(imdb_id=value).first()
    return movie.id