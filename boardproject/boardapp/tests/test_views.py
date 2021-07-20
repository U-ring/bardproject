from django.http import request, response
from django.test import TestCase
from django.urls import reverse, resolve
from boardapp.views import signupfunc
from ..models import User

# 下記usernameの重複テスト


class DuplicateSignUpTests(TestCase):
    def test_dont_create_user2(self):
        print("1です")
        url = reverse('signup')
        data = {
            'username': 'saigo',
            'password': 'saigo'
        }
        self.home_url = reverse('list')
        self.response = self.client.post(url, data)
        # 下記False
        self.assertRedirects(self.response, self.home_url, status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        userCount = User.objects.all().count()

        self.response = self.client.get('logout')
        self.response = self.client.post(url, data)
        userCount2 = User.objects.all().count()
        self.assertEquals(self.response.status_code, 200)
        self.assertEqual(userCount, userCount2)

# 下記サインアップ失敗時テスト


class InvalidSignUpTests(TestCase):
    def test_dont_create_user(self):
        print("2です")
        # ここから
        url = reverse('signup')
        data = {
            'username': 'saigo-',
            'password': 'saigo'
        }
        self.response = self.client.post(url, data)
        # ここまで
        self.assertEquals(self.response.status_code, 200)
        self.assertFalse(User.objects.exists())

# 下記サインアップのテスト


class SignupTests(TestCase):
    # def setUp(self):
    #     url = reverse('signup')
    #     self.response = self.client.get(url)

    def test_csrf(self):
        print("3です")
        url = reverse('signup')
        self.response = self.client.get(url)
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_signup_status_code(self):
        print("4です")
        url = reverse('signup')
        self.response = self.client.get(url)
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        print("5です")
        url = reverse('signup')
        self.response = self.client.get(url)
        view = resolve('/signup/')
        self.assertEquals(view.func, signupfunc)

# 下記サインアップ成功時のテスト


class SuccessfulSignUpTests(TestCase):
    def test_redirection(self):
        # print(self.response)
        # print(self.home_url)
        print("6です")
        # ここから
        url = reverse('signup')
        data = {
            'username': 'saigo',
            'password': 'saigo'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('list')
        # 下記False
        self.assertRedirects(self.response, self.home_url, status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
        # self.assertRedirects(self.response, self.home_url)

    def test_user_authentication(self):
        print("7です")
        # ここから
        url = reverse('signup')
        data = {
            'username': 'saigo',
            'password': 'saigo'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('list')
        # 下記、Falseを出力している
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

    def test_user_creation(self):
        print("8です")
        url = reverse('signup')
        data = {
            'username': 'saigo',
            'password': 'saigo'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('list')
        # ここまで
        self.assertTrue(User.objects.exists())
