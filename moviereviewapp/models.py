from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    rating = models.FloatField(null=True, blank=True, default=None)
    release_year = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title} ({self.release_year})'