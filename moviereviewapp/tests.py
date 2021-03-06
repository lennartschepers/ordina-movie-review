import http

import django.urls
import requests
from django.test import TestCase
from django.test.client import RequestFactory
from django.test import Client
from django.http import HttpResponse, HttpResponseServerError
from django.db.utils import IntegrityError

from .models import Movie, Review, User
from django.contrib import auth
from django.urls import reverse


class TestMainViews(TestCase):

    def test_views_can_be_requested(self):
        # given a movie with an id of 1 exists in the db
        movie = Movie.objects.create(title='test', description='', id=1, poster='tmp.jpeg')

        # and given the url of the index, movies, detail, register and addmovie views

        view_urls = [django.urls.reverse('index'), django.urls.reverse('movies'), django.urls.reverse('detail', kwargs={'movie_id': movie.id}),
                     django.urls.reverse('register'), django.urls.reverse('login'), django.urls.reverse('addmovie')]

        # when that page is requested
        for url in view_urls:
            response = self.client.get(url)

            # then the request succeeds
            self.assertEqual(response.status_code, http.HTTPStatus.OK)

class TestMovieDetailView(TestCase):

    def test_detail_view_shows_title(self):
        titles = ['Toy Story', 'Toy Story 2', 'Toy Story 3', 'Toy Story 4']
        # given a movie title
        for title in titles:

            # and a movie with that title in the database
            movie = Movie.objects.create(title=title, description='', poster='tmp.jpeg')
            # and a url to the detail view of that movie
            movie_url = django.urls.reverse('detail', kwargs={'movie_id': movie.id})

            # when that page is requested
            response = self.client.get(movie_url)

            # then the reponse contains the title of the movie
            with self.subTest(title=title):
                self.assertContains(response, title)

# try two variations of the same test, both don't seem to work:
class TestAuthentication(TestCase):

    def test_user_login(self):
        # given a user that exists in the database
        User = auth.get_user_model()
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()

        # when those credentials are passed in the login function
        login = self.client.login(username='testuser', password='12345')

        # the login function passes
        self.assertTrue(login)

class LogInTest(TestCase):

    # given a created user
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        # when a login request is sent with those credentials
        response = self.client.post('/accounts/login/', self.credentials, follow=True)
        # then should be logged in
        self.assertTrue(response.context['user'].is_authenticated)

class TestMovieAndReview(TestCase):
    # should probably be split in two seperate classes

    #given a movie in the db
    def setUp(self):
        self.movie_pk = Movie.objects.create(title='Test Title', description='Test Description', release_year=2021, poster='tmp/test.jpeg').id
        Review.objects.create(movie_id=self.movie_pk, body='lorem ipsum', rating=10)

    def test_movie_text_content(self):
        # when that movie is queried:
        movie = Movie.objects.get(pk=self.movie_pk)


        # that movie should be represented as title (release_year)
        expected_object_name = f'{movie.title} ({movie.release_year})'
        self.assertEquals(expected_object_name, 'Test Title (2021)')

    def test_review_cascade(self):
        movie = Movie.objects.filter(title='Test Title').first()
        review = Review.objects.filter(movie=movie).first()

        # when a movie is deleted
        movie.delete()
        review = Review.objects.filter(movie=movie).first()

        # the corresponding review that has that movie as fk should be deleted as well
        self.assertIsNone(review)

    def test_review_rating(self):
        movie = Movie.objects.get(pk=self.movie_pk)
        with self.assertRaises(IntegrityError) as context:
            Review.objects.create(movie_id=self.movie_pk, body='lorem ipsum', rating=15)
        self.assertTrue("A rating value is valid between 1 and 10"
                        in str(context.exception))

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




