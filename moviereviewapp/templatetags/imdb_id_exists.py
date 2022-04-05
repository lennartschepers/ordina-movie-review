from django import template
from moviereviewapp.models import Movie

register = template.Library()

@register.filter
def imdb_id_exists(value):
    """ checks if a movie exists with a corresponding imdb_id"""
    return Movie.objects.filter(imdb_id=value).exists()

