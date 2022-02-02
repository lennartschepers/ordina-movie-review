from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from .models import Movie

def index(request):
    return HttpResponse("Test index page")

def movies(request):
    movie_list = Movie.objects.all()
    context = {'movie_list': movie_list}
    return render(request, 'moviereviewapp/movies.html', context)

def  detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, 'moviereviewapp/detail.html', {'movie': movie})

