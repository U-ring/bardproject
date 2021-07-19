from django.http import request
from django.test import TestCase
from django.urls import reverse, resolve
from boardapp.views import signupfunc

from ..models import User

class SignupTests(TestCase):
    # def setUp(self):
    #     user = User.objects.create(username='testMan', password='testPass')

    # def test_get(self):
    #     response = self.client.get(reverse('signup'))
    #     self.assertEqual(response.status_code, 200)

    # def test_get_1users_by_list(self):
    #     response = self.client.get(reverse('signup'))
    #     self.assertEqual(response.status_code, 200)

    # 下記サインアップのテスト
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        # print("self.assertEquals(self.response.status_code, 200)は")
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup/')
        print("self.assertEquals(view.func, signupfunc)は")
        self.assertEquals(view.func, signupfunc)

    def test_csrf(self):
        # print("self.assertContains(self.response, 'csrfmiddlewaretoken')は")
        self.assertContains(self.response, 'csrfmiddlewaretoken')

# 下記サインアップ成功時のテスト
class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'saigo',
            'password': 'saigo'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('list')

    def test_redirection(self):
        print("self.assertRedirectsの上")
        print(self.response)
        print(self.home_url)
        self.assertRedirects(self.response, self.home_url)

    def test_user_creation(self):
        print("self.assertTrue(User.objects.exists())")
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):

        response = self.client.get(self.home_url)
        user = response.context.get('user')
        print("self.assertTrue(user.is_authenticated)の上")
        self.assertTrue(user.is_authenticated)

#下記サインアップ失敗時テスト
class InvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'saigo-',
            'password': 'saigo'
        }
        self.response = self.client.post(url, data)  # submit an empty dictionary

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())

    # 下記usernameの重複テスト
# class DuplicateSignUpTests(TestCase):
#     def setUp(self):
#         user = User.objects.create(username='saigo', password='saigo')
#         # user.save()
#         url = reverse('signup')
#         data = {
#             'username': 'saigo',
#             'password': 'saigo'
#         }
#         self.response = self.client.post(url, data)  # submit an empty dictionary

#     def test_dont_create_user2(self):
#         self.assertFalse(User.objects.exists())
