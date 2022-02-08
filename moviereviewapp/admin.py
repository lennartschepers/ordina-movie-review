from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Movie, Review, User

admin.site.register(User, UserAdmin)


class ReviewInline(admin.StackedInline):
    model = Review
    extra = 1


class MovieAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]


admin.site.register(Movie, MovieAdmin)


