from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from .forms import ReviewForm, SignInForm, RegisterForm, MovieForm
from .models import Movie
from  django.db.models import Q
import requests

def index(request):
    return HttpResponse("Test index page")

def movies(request):
    movie_query = request.GET.get('search')
    if movie_query:
        movie_list = Movie.objects.filter(Q(title__icontains=movie_query) | Q(description__icontains=movie_query))
    else:
        movie_list = Movie.objects.all().order_by('-id')
    context = {'movie_list': movie_list, 'movie_query': movie_query}
    return render(request, 'moviereviewapp/movies.html', context)

def  detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.save()
        else:
            return render(request, 'moviereviewapp/detail.html', {'movie': movie, 'form': form})

    form = ReviewForm()
    # range binding for rating stars in reviews
    return render(request, 'moviereviewapp/detail.html', {'movie': movie, 'form': form})

def signin(request):
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return render(request, '', {'form': form})
    form = SignInForm()
    return render(request, '', {'form': form})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(movies)
        else:
            return render(request, 'moviereviewapp/register.html', {'form': form})
    form = RegisterForm()
    return render(request, 'moviereviewapp/register.html', {'form': form})

def addmovie(request):
    api_query = request.GET.get('search_api')
    if api_query:
        api_results = requests.get('https://imdb-api.com/en/API/SearchMovie/k_xq770k6q/' + api_query).json()['results']
    else:
        api_results = None

    if request.method == "POST":
        movie_id = request.POST.get('movie_id')
        detailed_res = requests.get('https://imdb-api.com/en/API/SearchMovie/k_xq770k6q/' + movie_id).json()
        movie = {
            'title': detailed_res.title,
            'description': detailed_res.plot,
            'release_year': detailed_res.releaseDate,
        }
        form = MovieForm(movie, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(movies)
        else:
            return render(request, 'moviereviewapp/register.html', {'form': form})
    form = MovieForm
    return render(request, 'moviereviewapp/addmovie.html', {'form': form, 'api_results': api_results})