from django.test import TestCase
from .models import User, Team, Activity, Leaderboard, Workout

class ModelTests(TestCase):
    def setUp(self):
        marvel = Team.objects.create(name='Marvel')
        tony = User.objects.create(name='Tony Stark', email='tony@marvel.com', team=marvel)
        Activity.objects.create(user=tony, type='Run', duration=30, calories=300)
        Workout.objects.create(name='Avenger HIIT', description='High intensity workout for Marvel heroes')
        Leaderboard.objects.create(user=tony, points=1000)

    def test_user(self):
        self.assertEqual(User.objects.count(), 1)

    def test_team(self):
        self.assertEqual(Team.objects.count(), 1)

    def test_activity(self):
        self.assertEqual(Activity.objects.count(), 1)

    def test_workout(self):
        self.assertEqual(Workout.objects.count(), 1)

    def test_leaderboard(self):
        self.assertEqual(Leaderboard.objects.count(), 1)
