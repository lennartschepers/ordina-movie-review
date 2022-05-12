from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("movies/", views.Movies.as_view(), name="movies"),
    path("movies/<int:movie_id>/", views.detail, name="detail"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("registration/register", views.register, name="register"),
    path("addmovie/", views.addmovie, name="addmovie"),
]
