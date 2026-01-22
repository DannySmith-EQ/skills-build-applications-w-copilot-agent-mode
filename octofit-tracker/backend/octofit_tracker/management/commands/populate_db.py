from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models
from octofit_tracker.models import Team, Activity, Leaderboard, Workout

from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Deleting old data...'))
        User = get_user_model()
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Creating teams...'))
        marvel = Team.objects.create(name='Team Marvel')
        dc = Team.objects.create(name='Team DC')

        self.stdout.write(self.style.SUCCESS('Creating users...'))
        users = [
            User(email='ironman@marvel.com', username='ironman', team=marvel),
            User(email='captainamerica@marvel.com', username='captainamerica', team=marvel),
            User(email='batman@dc.com', username='batman', team=dc),
            User(email='superman@dc.com', username='superman', team=dc),
        ]
        for user in users:
            user.set_password('password')
            user.save()

        self.stdout.write(self.style.SUCCESS('Creating activities...'))
        Activity.objects.create(user=users[0], type='run', duration=30, distance=5)
        Activity.objects.create(user=users[1], type='cycle', duration=45, distance=20)
        Activity.objects.create(user=users[2], type='swim', duration=60, distance=2)
        Activity.objects.create(user=users[3], type='walk', duration=90, distance=8)

        self.stdout.write(self.style.SUCCESS('Creating workouts...'))
        Workout.objects.create(name='Morning Cardio', description='A quick morning run', suggested_for=marvel)
        Workout.objects.create(name='Strength Training', description='Weight lifting', suggested_for=dc)

        self.stdout.write(self.style.SUCCESS('Creating leaderboard...'))
        Leaderboard.objects.create(user=users[0], score=100)
        Leaderboard.objects.create(user=users[1], score=90)
        Leaderboard.objects.create(user=users[2], score=95)
        Leaderboard.objects.create(user=users[3], score=85)

        self.stdout.write(self.style.SUCCESS('Ensuring unique index on user email...'))
        with connection.cursor() as cursor:
            cursor.db_conn['users'].create_index('email', unique=True)

        self.stdout.write(self.style.SUCCESS('Database populated with test data!'))

# Models for reference (should be in octofit_tracker/models.py):
# class Team(models.Model):
#     name = models.CharField(max_length=100)
#
# class Activity(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     type = models.CharField(max_length=50)
#     duration = models.IntegerField()
#     distance = models.FloatField()
#
# class Workout(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     suggested_for = models.ForeignKey(Team, on_delete=models.CASCADE)
#
# class Leaderboard(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     score = models.IntegerField()
