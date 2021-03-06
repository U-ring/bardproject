from django.test import TestCase
from boardapp.models import User, Profile

class UserModelTests(TestCase):

    def test_is_empty(self):
        saved_users = User.objects.all()
        self.assertEqual(saved_users.count(), 0)

    def test_is_count_one(self):
        user = User(username='testLady', password='testPassword')
        user.save()
        saved_users = User.objects.all()
        saved_profiles = Profile.objects.all()
        self.assertEqual(saved_users.count(), 1)
        self.assertEqual(saved_profiles.count(), 1)
