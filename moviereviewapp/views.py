import os.path

import requests
from django.contrib.auth import login
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import Q
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render, get_object_or_404, redirect

from .forms import ReviewForm, SignInForm, RegisterForm, MovieForm
from .models import Movie


def index(request):
    return HttpResponse("Test index page")


def movies(request):
    movie_query = request.GET.get("search")
    if movie_query:
        movie_list = Movie.objects.filter(
            Q(title__icontains=movie_query) | Q(description__icontains=movie_query)
        )
    else:
        movie_list = Movie.objects.all().order_by("-id")
    context = {"movie_list": movie_list, "movie_query": movie_query}
    return render(request, "moviereviewapp/movies.html", context)


def detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.save()
        else:
            return render(
                request, "moviereviewapp/detail.html", {"movie": movie, "form": form}
            )

    form = ReviewForm()
    # range binding for rating stars in reviews
    return render(request, "moviereviewapp/detail.html", {"movie": movie, "form": form})


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
            return HttpResponseServerError('invalid response from img url, ID is wrong or API limit is exceeded')

        movie = {
            "title": detailed_res["title"],
            "description": detailed_res["plot"],
            "release_year": detailed_res["year"],
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
