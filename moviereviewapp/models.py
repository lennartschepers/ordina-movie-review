from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg, Q
from django.urls import reverse


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1500)
    release_year = models.IntegerField(default=0)
    poster = models.ImageField()
    runtime = models.CharField(blank=True, max_length=20)
    genres = models.CharField(blank=True, max_length=200)
    directors = models.CharField(blank=True, max_length=200)
    writers = models.CharField(blank=True, max_length=200)
    stars = models.CharField(blank=True, max_length=200)
    awards = models.CharField(blank=True, max_length=200)
    imdb_rating = models.CharField(blank=True, max_length=20)
    metacritic_rating = models.CharField(blank=True, max_length=20)
    similars = models.TextField(blank=True)
    imdb_id = models.CharField(blank=True, max_length=20)


    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.title} ({self.release_year})"

    @property
    def average_rating(self):
        print(self.review_set.all().aggregate(Avg('rating')).get('rating__avg'))
        return self.review_set.all().aggregate(Avg('rating')).get('rating__avg')

     # def get_url_if_imdb_id_exists(self, imdb_id):
     #    if Movie.objects.filter(imdb_id=imdb_id):
     #         ordina_id = Movie.objects.filter(imdb_id=imdb_id)
     #         return reverse('detail', kwargs={'movie_id': ordina_id})
     #    else:
     #        return None

class Review(models.Model):
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(rating__gte=1) & models.Q(rating__lte=10),
                name="A rating value is valid between 1 and 10"
            )
        ]

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
