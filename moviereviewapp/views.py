from django.http import HttpResponse
from django.shortcuts import render
from .models import Movie

def index(request):
    return HttpResponse("Test index page")

def movies(request):
    movie_list = Movie.objects.all()
    context = {'movie_list': movie_list}
    return render(request, 'moviereviewapp/movies.html', context)

