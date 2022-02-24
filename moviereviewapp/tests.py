import http

import django.urls
from django.test import TestCase
from .models import Movie

# Create your tests here.
class TestMovie(TestCase):

    def test_index_page_can_be_requested(self):
        # given the url of the index page
        index_url = django.urls.reverse('index')

        # when that page is requested
        response = self.client.get(index_url)

        # then the request succeeds
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

class TestMovieDetailView(TestCase):

    def test_detail_view_shows_title(self):
        titles = ['Toy Story', 'Toy Story 2', 'Toy Story 3', 'Toy Story 4']
        # given a movie title
        #title = 'Inception'
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