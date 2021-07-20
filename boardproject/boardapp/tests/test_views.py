from django.http import request, response
from django.test import TestCase
from django.urls import reverse, resolve
from boardapp.views import signupfunc
from ..models import User

# 下記usernameの重複テスト


class DuplicateSignUpTests(TestCase):

    def setUp(self):
        User(username='saigo', password='saigo').save()

    # 既に存在するusernameでユーザー登録しようとした場合、登録完了画面である/list/にリダイレクトしない、かつuser登録がされないことをテストするメソッド
    def test_dont_create_user2(self):
        userCount = User.objects.all().count()

        url = reverse('signup')
        data = {
            'username': 'saigo',
            'password': 'saigo'
        }
        self.response = self.client.get('logout')
        self.response = self.client.post(url, data)
        userCount2 = User.objects.all().count()
        self.assertEquals(self.response.status_code, 200)
        self.assertEqual(userCount, userCount2)

    def tearDown(self):
        User.objects.all().delete()

# 下記サインアップ失敗時テスト


class InvalidSignUpTests(TestCase):

    # usernameに無効文字「-」が入っていた場合、登録完了画面である/list/にリダイレクトしない、かつuser登録がされないことをテストするメソッド
    def test_dont_create_user(self):
        url = reverse('signup')
        data = {
            'username': 'saigo-',
            'password': 'saigo'
        }
        self.response = self.client.post(url, data)
        self.assertEquals(self.response.status_code, 200)
        self.assertFalse(User.objects.exists())

    def tearDown(self):
        User.objects.all().delete()

# 下記サインアップのテスト


class SignupTests(TestCase):

    # CSRF対策のトークンが含まれているかのテストメソッド
    def test_csrf(self):
        url = reverse('signup')
        self.response = self.client.get(url)
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    # signupページへの遷移が無事行われているかのテストメソッド
    def test_signup_status_code(self):
        url = reverse('signup')
        self.response = self.client.get(url)
        self.assertEquals(self.response.status_code, 200)

    # signupのURLパスとview関数がマッピングしているかのテストメソッド
    def test_signup_url_resolves_signup_view(self):
        url = reverse('signup')
        self.response = self.client.get(url)
        view = resolve('/signup/')
        self.assertEquals(view.func, signupfunc)

    def tearDown(self):
        User.objects.all().delete()

# 下記サインアップ成功時のテスト


class SuccessfulSignUpTests(TestCase):

    # ユーザー登録成功した際に/list/にリダイレクトがされているかをテストするメソッド
    def test_redirection(self):
        url = reverse('signup')
        data = {
            'username': 'saigo',
            'password': 'saigo'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('list')
        self.assertRedirects(self.response, self.home_url, status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    # ユーザー登録と同時にそのユーザーがログインに成功しているかをテストするメソッド
    def test_user_authentication(self):
        url = reverse('signup')
        data = {
            'username': 'saigo',
            'password': 'saigo'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('list')

        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

    # ユーザー登録と同時にそのユーザーのレコードがDBに保存されているかをテストするメソッド
    def test_user_creation(self):
        url = reverse('signup')
        data = {
            'username': 'saigo',
            'password': 'saigo'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('list')

        self.assertTrue(User.objects.filter(username='saigo').exists())

    def tearDown(self):
        User.objects.all().delete()
