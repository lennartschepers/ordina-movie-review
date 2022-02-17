from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from .forms import ReviewForm, SignInForm, RegisterForm, MovieForm
from .models import Movie

def index(request):
    return HttpResponse("Test index page")

def movies(request):
    movie_list = Movie.objects.all().order_by('id').reverse()
    context = {'movie_list': movie_list}
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
    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(movies)
        else:
            return render(request, 'moviereviewapp/register.html', {'form': form})
    form = MovieForm
    return render(request, 'moviereviewapp/addmovie.html', {'form': form})