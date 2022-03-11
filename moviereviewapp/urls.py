from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("movies/", views.movies, name="movies"),
    path("movies/<int:movie_id>/", views.detail, name="detail"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("registration/register", views.register, name="register"),
    path("addmovie/", views.addmovie, name="addmovie"),
]
