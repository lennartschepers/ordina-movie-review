from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1500)
    rating = models.FloatField(null=True, blank=True, default=None)
    release_year = models.IntegerField(default=0)
    poster = models.ImageField()

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.title} ({self.release_year})"


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


class User(AbstractUser):
    pass
