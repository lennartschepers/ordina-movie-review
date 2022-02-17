# Generated by Django 4.0.1 on 2022-02-10 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviereviewapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='release_year',
        ),
        migrations.AddField(
            model_name='movie',
            name='poster',
            field=models.ImageField(default='images/posters/default.jpg', upload_to='images/posters'),
        ),
    ]