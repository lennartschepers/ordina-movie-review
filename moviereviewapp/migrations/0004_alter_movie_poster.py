# Generated by Django 4.0.1 on 2022-02-10 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviereviewapp', '0003_movie_release_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='poster',
            field=models.ImageField(default='static/images/posters/default.jpg', upload_to='images/posters'),
        ),
    ]