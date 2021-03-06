# Generated by Django 4.0.2 on 2022-03-29 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moviereviewapp', '0007_remove_movie_rating_alter_movie_description_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='review',
            constraint=models.CheckConstraint(check=models.Q(('rating__gte', 1), ('rating__lte', 10)), name='A rating value is valid between 1 and 10'),
        ),
    ]
