from django.db import models
from datetime import datetime


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    rating = models.FloatField(null=True, blank=True, default=None)
    release_year = models.IntegerField(default=0)
    poster = models.ImageField(upload_to='movies/', height_field=None, width_field=None, default='movies/default.jpg')

    def __str__(self):
        return f'{self.title} ({self.release_year})'


class Review(models.Model):

    class Rating(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    body = models.TextField()
    rating = models.IntegerField(null=False, blank=False, choices=Rating.choices)




