import http

import django.urls
from django.test import TestCase
from .models import Movie, Review
from django.contrib import auth
from django.urls import reverse
import requests
from django.test.client import RequestFactory
from django.test import Client
from django.http import HttpResponse, HttpResponseServerError
from .models import Movie

# Create your tests here.

# vragen: test ik genoeg, moet ik bij exceptions een bericht printen of een httpresponse returnen

class TestMoviePost(TestCase):
    def test_movie_post(self):
        """
        test if a movie can be added to the db, given a valid id
        """
        client = Client()
        data = {'movie_id': 'tt1321322'}
        response = client.post(reverse('addmovie'), data=data)
        self.assertEqual(Movie.objects.count(), 1)

    def test_movie_post_invalid_id(self):
        """
        if the movie_id is invalid, or the api limit is reached, the 'detailed_res' is going to be an error messaged
        and should be handled as such
        """
        client = Client()
        data = {'movie_id': '00000'}
        response = client.post(reverse('addmovie'), data=data)
        print(response)
        self.assertEqual(Movie.objects.count(), 0)

    def test_movie_post_duplicate(self):
        """
        Test if an existing movie can not posted again
        """
        client = Client()
        data = {'movie_id': 'tt1321322'}
        response = client.post(reverse('addmovie'), data=data)
        data = {'movie_id': 'tt1321322'}
        response = client.post(reverse('addmovie'), data=data)
        self.assertEqual(Movie.objects.count(), 1)




