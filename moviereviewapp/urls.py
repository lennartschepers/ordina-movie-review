from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('movies/', views.movies, name='movies'),
    path('movies/<int:movie_id>/', views.detail, name='detail'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('registration/register', views.register, name='register'),

]

