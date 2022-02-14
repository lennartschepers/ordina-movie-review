#!/usr/bin/env bash
python manage.py migrate
gunicorn ordina_movie_review.wsgi:application -b 0.0.0.0:8000