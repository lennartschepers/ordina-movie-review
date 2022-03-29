from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    release_year = models.IntegerField(default=0)
    poster = models.ImageField()

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.title} ({self.release_year})"

    @property
    def average_rating(self):
        print(self.review_set.all().aggregate(Avg('rating')).get('rating__avg'))
        return self.review_set.all().aggregate(Avg('rating')).get('rating__avg')


class Review(models.Model):
    class Rating(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5
        SIX = 6
        SEVEN = 7
        EIGHT = 8
        NINE = 9
        TEN = 10

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    body = models.TextField()
    rating = models.IntegerField(null=False, blank=False, choices=Rating.choices)


class User(AbstractUser):
    pass
