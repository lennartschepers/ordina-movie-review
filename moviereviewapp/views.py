import os.path

import requests
import ast
from django.contrib.auth import login
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import Q
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render, get_object_or_404, redirect

from .forms import ReviewForm, SignInForm, RegisterForm, MovieForm
from .models import Movie, Review, User
from django.core.paginator import Paginator
from django.views import View
from django.views.generic import ListView


class Index(View):
    def get(self, request):
        return HttpResponse("Test index page")


class Movies(ListView):
    template_name = "moviereviewapp/movies.html"
    model = Movie
    paginate_by = 10

    def get_queryset(self):
        self.query = self.request.GET.get('search')
        self.sort = self.request.GET.get('movie_sort')
        if self.query:
            movie_list = Movie.objects.filter(
                Q(title__icontains=self.query) | Q(description__icontains=self.query)
            )
        else:
            movie_list = Movie.objects.all().order_by("-id")
        if self.sort is None or self.sort == 'latest':
            movie_list = movie_list.order_by("-id")
        elif self.sort == 'oldest':
            movie_list = movie_list.order_by("id")
        return movie_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie_query'] = self.query
        context['movie_sort'] = self.sort
        return context


def detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    movie.genres = [genre.strip() for genre in movie.genres.split(',')]
    movie.awards = movie.awards.split(',')

    # make dictionary with imdb_id as key, Ordina id and average rating as values to check for existing similar movies
    id_by_imdb_id = Movie.objects.all().values_list('imdb_id', 'id')
    imdb_id_dict = {tuple[0]: [tuple[1]] for tuple in id_by_imdb_id}
    for id in imdb_id_dict:
        average_rating = Movie.objects.get(pk=imdb_id_dict[id][0]).average_rating
        imdb_id_dict[id].append(average_rating)

    if movie.similars:
        movie.similars = ast.literal_eval(movie.similars)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.username = request.user.username
            review.save()
        else:
            print(form.errors)
            return render(
                request, "moviereviewapp/detail.html", {"movie": movie, "form": form}
            )

    form = ReviewForm()
    return render(request, "moviereviewapp/detail.html", {"movie": movie, "form": form,
                                                          "imdb_id_dict": imdb_id_dict})


def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    reviews = Review.objects.filter(username=username)
    return render(request, "moviereviewapp/profile.html", {"profile_user": profile_user, "reviews": reviews})


def signin(request):
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return render(request, "", {"form": form})
    form = SignInForm()
    return render(request, "", {"form": form})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(movies)
        else:
            return render(request, "moviereviewapp/register.html", {"form": form})
    form = RegisterForm()
    return render(request, "moviereviewapp/register.html", {"form": form})

def save_image(url, movie_id):
    image_request = requests.get(url, stream=True)
    image_tmp = None
    if image_request.status_code == 200:
        _, _, filename = url.rpartition("/")
        _, ext = os.path.splitext(filename)
        storage_file_name = f"{movie_id}{ext}"
        image_tmp = SimpleUploadedFile(
            name=storage_file_name,
            content_type=image_request.headers["Content-Type"],
            content=image_request.content,
        )
    return image_tmp


def addmovie(request):
    api_query = request.GET.get("search_api")
    if api_query:
        api_results = requests.get(
            "https://imdb-api.com/en/API/SearchMovie/k_xq770k6q/" + api_query
        ).json()["results"]
    else:
        api_results = None

    if request.method == "POST":
        movie_id = request.POST.get("movie_id")

        detailed_res = requests.get(
            "https://imdb-api.com/en/API/Title/k_xq770k6q/" + movie_id
        ).json()

        if Movie.objects.filter(title=detailed_res["title"]).exists():
            print("movie already exists")
            return redirect(movies)

        img_url = detailed_res['image']
        try:
            img_temp = save_image(
                url=img_url,
                movie_id=movie_id
            )
        except requests.exceptions.MissingSchema:
            print('invalid response from img url, ID is wrong or API limit is exceeded')
            print('the id is: ' + movie_id)
            return HttpResponseServerError('invalid response from img url, ID is wrong or API limit is exceeded')

        movie = {
            "title": detailed_res["title"],
            "description": detailed_res["plot"],
            "release_year": detailed_res["year"],
            "genres": detailed_res["genres"],
            "directors": detailed_res["directors"],
            "writers": detailed_res["writers"],
            "stars": detailed_res["stars"],
            "awards": detailed_res["awards"],
            "imdb_rating": detailed_res["imDbRating"],
            "metacritic_rating": detailed_res["metacriticRating"],
            "runtime": detailed_res["runtimeStr"],
            "similars": detailed_res["similars"],
            "imdb_id": detailed_res["id"]
        }

        form = MovieForm(movie)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.poster = img_temp
            instance.save()
            return redirect(movies)
        else:
            print(form.errors)
            return render(
                request,
                "moviereviewapp/addmovie.html",
                {"form": form, "api_results": api_results},
            )
    form = MovieForm
    return render(
        request,
        "moviereviewapp/addmovie.html",
        {"form": form, "api_results": api_results},
    )
