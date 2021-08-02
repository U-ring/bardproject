from django.http import request, response
from django.test import TestCase
import unittest
from django.urls import reverse, resolve
from boardapp.views import signupfunc, loginfunc
from ..models import User, Likes, Nopes, Messages
from asgiref.sync import async_to_sync, sync_to_async
import asyncio
import async_timeout
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.testing import HttpCommunicator, WebsocketCommunicator
from boardapp.consumers import ChatConsumer
import datetime
import sqlite3 
import traceback
import json

from django.core.files.uploadedfile import SimpleUploadedFile
import os

# 下記usernameの重複テスト


class DuplicateSignUpTests(TestCase):

    def setUp(self):
        user = User.objects.create_user('saigo', '', 'saigo')
        user.profile.gender = '男性'
        user.profile.save()

    # 既に存在するusernameでユーザー登録しようとした場合、登録完了画面である/list/にリダイレクトしない、かつuser登録がされないことをテストするメソッド
    def test_dont_create_user2(self):
        userCount = User.objects.all().count()

        url = reverse('signup')
        data = {
            'username': 'saigo',
            'password': 'saigo',
            'gender': '男性'
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
            'password': 'saigo',
            'gender': '男性'
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
            'password': 'saigo',
            'gender': '男性'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('list')
        self.assertRedirects(self.response, self.home_url, status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    # ユーザー登録と同時にそのユーザーがログインに成功しているかをテストするメソッド
    def test_user_authentication(self):
        url = reverse('signup')
        data = {
            'username': 'saigo',
            'password': 'saigo',
            'gender': '男性'
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
            'password': 'saigo',
            'gender': '男性'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('list')

        self.assertTrue(User.objects.filter(username='saigo').exists())

    def tearDown(self):
        User.objects.all().delete()


# ユーザーログインに関することをテストするクラス
class loginTest(TestCase):
    def setUp(self):
        user = User.objects.create_user('saigo', '', 'saigo')
        user.profile.gender = '男性'
        user.profile.save()

    # ログイン成功時に「/list/」にアクセス（リダイレクト）していることをテストするメソッド。
    def test_when_loginRedirect_List(self):
        url = reverse('login')
        data = {
            'username': 'saigo',
            'password': 'saigo'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('list')
        self.assertRedirects(self.response, self.home_url, status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    # 誤入力によるログイン失敗時「/login/」に再アクセスすることをテストするメソッド。
    def test_when_miss_password_and_username(self):
        url = reverse('login')
        data = {
            'username': 'saigo',
            'password': 'saigooo'
        }
        self.response = self.client.post(url, data)

        self.assertEquals(self.response.status_code, 200)

        url = reverse('login')
        data = {
            'username': 'saigooo',
            'password': 'saigo'
        }
        self.response = self.client.post(url, data)

        self.assertEquals(self.response.status_code, 200)

    def tearDown(self):
        User.objects.all().delete()


# /list/でのテスト
class listTests(TestCase):
    def setUp(self):
        user = User.objects.create_user('saigo', '', 'saigo')
        user.profile.gender = '男性'
        user.profile.save()

        user2 = User.objects.create_user('suzuki', '', 'suzuki')
        user2.profile.gender = '男性'
        user2.profile.save()

        user3 = User.objects.create_user('sato', '', 'sato')
        user3.profile.gender = '女性'
        user3.profile.save()

    # /list/において異性が表示されることをテストするメソッド
    def test_list(self):
        url = reverse('login')
        data = {
            'username': 'saigo',
            'password': 'saigo'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('list')
        afterLoginResponse = self.client.get(self.home_url)
        self.assertEqual(afterLoginResponse.context['nextUser'].profile.gender, "女性")

    # /list/において同性が表示されないことをテストするメソッド
    def test_list_noDisplay_same_sex(self):
        url = reverse('login')
        data = {
            'username': 'saigo',
            'password': 'saigo'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('list')
        beforeLikeResponse = self.client.get(self.home_url)
        self.assertEqual(beforeLikeResponse.context['nextUser'].profile.gender, '女性')
        likeurl = reverse('like', kwargs={'pk': beforeLikeResponse.context['nextUser'].id})
        self.response = self.client.post(likeurl)
        afterLikeResponse = self.client.get(self.home_url)
        self.assertEqual(afterLikeResponse.context['nextUser'], None)

    def tearDown(self):
        User.objects.all().delete()


# likeにおけるテストクラス
class LikeTests(TestCase):
    def setUp(self):
        user = User.objects.create_user('saigo', '', 'saigo')
        user.profile.gender = '男性'
        user.profile.save()

        user2 = User.objects.create_user('sato', '', 'sato')
        user2.profile.gender = '女性'
        user2.profile.save()

    # likeを押した際にモデルLikesに1件レコードが追加されることをテストするメソッド
    def test_click_like_whether_saved(self):
        url = reverse('login')
        data = {
            'username': 'saigo',
            'password': 'saigo'
        }
        self.assertEqual(Likes.objects.all().count(),0)
        self.response = self.client.post(url, data)
        self.home_url = reverse('list')
        beforeLikeResponse = self.client.get(self.home_url)
        likeurl = reverse('like', kwargs={'pk': beforeLikeResponse.context['nextUser'].id})
        self.response = self.client.post(likeurl)
        self.assertEqual(Likes.objects.filter(user_id=User.objects.filter(username="saigo").get().id, liked_user_id=beforeLikeResponse.context['nextUser'].id).count(), 1)

    # likeクリック後/list/にリダイレクトされることをテストするメソッド
    def test_after_like_redirect(self):
        url = reverse('login')
        data = {
            'username': 'saigo',
            'password': 'saigo'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('list')
        beforeLikeResponse = self.client.get(self.home_url)
        likeurl = reverse('like', kwargs={'pk': beforeLikeResponse.context['nextUser'].id})
        self.response = self.client.post(likeurl)
        self.assertRedirects(self.response, self.home_url, status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    # likeクリックによるマッチング発生時、マッチング通知画面に遷移するかテストするメソッド。
    def test_matching_redirect(self):
        like = Likes(user_id=2, liked_user_id=1)
        like.save()
        url = reverse('login')
        data = {
            'username': 'saigo',
            'password': 'saigo'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('list')

        likeurl = reverse('like', kwargs={'pk': 2})
        self.response = self.client.post(likeurl)
        response = self.client.get(self.home_url)

        self.assertTemplateUsed(response, 'matching.html')

    def tearDown(self):
        User.objects.all().delete()
        Likes.objects.all().delete()


# 「/list/」におけるユーザーNope（興味なし）ボタンに関するテストクラス。
class NopeTests(TestCase):
    def setUp(self):
        user = User.objects.create_user('saigo', '', 'saigo')
        user.profile.gender = '男性'
        user.profile.save()

        user2 = User.objects.create_user('sato', '', 'sato')
        user2.profile.gender = '女性'
        user2.profile.save()

    # nopeを押した際にモデルNopesに1件レコードが追加されることをテストするメソッド
    def test_click_nope_whether_saved(self):
        url = reverse('login')
        data = {
            'username': 'saigo',
            'password': 'saigo'
        }
        self.assertEqual(Nopes.objects.all().count(), 0)
        self.response = self.client.post(url, data)
        self.home_url = reverse('list')
        beforeNopeResponse = self.client.get(self.home_url)
        nopeurl = reverse('nope', kwargs={'pk': beforeNopeResponse.context['nextUser'].id})
        self.response = self.client.post(nopeurl)
        self.assertEqual(Nopes.objects.filter(user_id=User.objects.filter(username="saigo").get().id, noped_user_id=beforeNopeResponse.context['nextUser'].id).count(), 1)

    # nopeクリック後に/list/にリダイレクトされることをテストするメソッド
    def test_after_noped_redirect(self):
        url = reverse('login')
        data = {
            'username': 'saigo',
            'password': 'saigo'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('list')
        beforeNopeResponse = self.client.get(self.home_url)
        nopeurl = reverse('nope', kwargs={'pk': beforeNopeResponse.context['nextUser'].id})
        self.response = self.client.post(nopeurl)
        self.assertRedirects(self.response, self.home_url, status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    def tearDown(self):
        User.objects.all().delete()
        Nopes.objects.all().delete()


# 「/matchinglist/」における動作に関連するものをテストするクラス。
class MatchingListTest(TestCase):
    def setUp(self):
        user = User.objects.create_user('saigo', '', 'saigo')
        user.profile.gender = '男性'
        user.profile.save()

        user2 = User.objects.create_user('sato', '', 'sato')
        user2.profile.gender = '女性'
        user2.profile.save()

        user3 = User.objects.create_user('suzuki', '', 'suzuki')
        user3.profile.gender = '女性'
        user3.profile.save()

    # 「/matchinglist/」への正常なアクセスが可能であることをテストするメソッド。
    def test_matchingList_status_code(self):
        url = reverse('login')
        data = {
            'username': 'saigo',
            'password': 'saigo',
            'gender': '男性'
        }
        self.response = self.client.post(url, data)

        url = reverse('matchinglist')
        self.response = self.client.get(url)
        self.assertEquals(self.response.status_code, 200)

    # 「/matchinglist/」に表示されるユーザーが、マッチングしたユーザーであることをテストするメソッド。
    def test_matchinglist_display(self):
        like = Likes(user_id=1, liked_user_id=2)
        like.save()
        like = Likes(user_id=2, liked_user_id=1)
        like.save()
        like = Likes(user_id=1, liked_user_id=3)
        like.save()
        like = Likes(user_id=3, liked_user_id=1)
        like.save()

        url = reverse('login')
        data = {
            'username': 'saigo',
            'password': 'saigo',
            'gender': '男性'
        }
        self.response = self.client.post(url, data)

        url = reverse('matchinglist')
        self.response = self.client.get(url)
        self.assertEquals(len(self.response.context['matchingList']), 2)
        self.assertEquals(self.response.context['matchingList'][0].username, 'sato')
        self.assertEquals(self.response.context['matchingList'][1].username, 'suzuki')

    def tearDown(self):
        User.objects.all().delete()
        Likes.objects.all().delete()


# 「/machinglist/」におけるマッチング解除機能に関係するものをテストするクラス。
class DeleteMatchingTest(TestCase):
    def setUp(self):
        user = User.objects.create_user('saigo', '', 'saigo')
        user.profile.gender = '男性'
        user.profile.save()

        user2 = User.objects.create_user('sato', '', 'sato')
        user2.profile.gender = '女性'
        user2.profile.save()

        like = Likes(user_id=1, liked_user_id=2)
        like.save()
        like = Likes(user_id=2, liked_user_id=1)
        like.save()

    # マッチング解除機能が正常に動作することをテストするメソッド。
    def test_deleteMatching(self):
        self.assertEqual(Likes.objects.all().count(), 2)
        url = reverse('login')
        data = {
            'username': 'saigo',
            'password': 'saigo',
            'gender': '男性'
        }
        self.response = self.client.post(url, data)
        data = {
            'matchingUserId': 2
        }
        url = reverse('deleteMatching')
        self.response = self.client.post(url, data)
        self.assertEquals(Likes.objects.all().count(), 1)

    # マッチング解除後に「/list/」にリダイレクトしていることをテストするメソッド。
    def test_deleteMatching_status_code(self):
        url = reverse('login')
        data = {
            'username': 'saigo',
            'password': 'saigo',
            'gender': '男性'
        }
        self.response = self.client.post(url, data)
        data = {
            'matchingUserId': 2
        }
        url = reverse('deleteMatching')
        self.response = self.client.post(url, data)
        url = reverse('matchinglist')
        self.assertRedirects(self.response, url, status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

        def tearDown(self):
            User.objects.all().delete()
            Likes.objects.all().delete()


# 「/」の中でも特にhttp通信しているメソッドやcontextに関するものをテストするクラス。
class ChatContextTest(TestCase):
    def setUp(self):
        user = User.objects.create_user('saigo', '', 'saigo')
        user.profile.gender = '男性'
        user.profile.save()

        user2 = User.objects.create_user('sato', '', 'sato')
        user2.profile.gender = '女性'
        user2.profile.save()

        like = Likes(user_id=1, liked_user_id=2)
        like.save()
        like = Likes(user_id=2, liked_user_id=1)
        like.save()

    # チャットルームである「/」に対して正常にアクセスできているかテストするメソッド。
    def test_status_code(self):

        url = reverse('login')
        data = {
            'username': 'saigo',
            'password': 'saigo'
        }

        self.response = self.client.post(url, data)

        data = {
            'talkToId': 2
        }
        url = reverse('chat')
        self.response = self.client.post(url, data)
        self.assertEqual(self.response.status_code, 200)

    # chatのルーム名を一意かつ正しく「/」に対してパラメータとして渡せているかテストするメソッド。Tはuser_idの区切り文字である。
    def test_roomname(self):
        self.assertEqual(Likes.objects.all().count(), 2)

        url = reverse('login')
        data = {
            'username': 'saigo',
            'password': 'saigo'
        }

        self.response = self.client.post(url, data)

        data = {
            'talkToId': 2
        }
        url = reverse('chat')
        self.response = self.client.post(url, data)
        saigoRoomName = self.response.context.get('room')

        self.response = self.client.get(reverse('logout'))

        url = reverse('login')
        data = {
            'username': 'sato',
            'password': 'sato'
        }
        self.response = self.client.post(url, data)

        data = {
            'talkToId': 1
        }
        url = reverse('chat')
        self.response = self.client.post(url, data)
        satoRoomName = self.response.context.get('room')
        self.assertEqual(saigoRoomName, satoRoomName)

    # room名以外のパラメータが「/」に対して正しく渡せているかテストするメソッド。
    def test_chat_context(self):
        self.assertEqual(Likes.objects.all().count(), 2)

        message = Messages(room_name="1T2", user_id=1, talk_user_id=2, message="messageFrom1")
        message.save()
        message2 = Messages(room_name="2T1", user_id=2, talk_user_id=1, message="messageFrom2")
        message2.save()

        url = reverse('login')
        data = {
            'username': 'saigo',
            'password': 'saigo'
        }

        self.response = self.client.post(url, data)

        data = {
            'talkToId': 2
        }
        url = reverse('chat')
        self.response = self.client.post(url, data)

        self.assertEqual(self.response.context.get('user').id, 1)
        self.assertEqual(self.response.context.get('talkTo').id, 2)
        self.assertEqual(self.response.context.get('messages')[0]['username'], 'saigo')
        self.assertEqual(self.response.context.get('messages')[0]['message'], 'messageFrom1')
        dtNow = datetime.datetime.now()
        self.assertEqual(self.response.context.get('messages')[0]['date'][:13], str(dtNow.strftime('%Y/%m/%d %H')))

    # チャットをするお互いのユーザーのidが「/」に対して正しく渡せているかテストするメソッド
    def test_match_talk_user(self):
        self.assertEqual(Likes.objects.all().count(), 2)

        message = Messages(room_name="1T2", user_id=1, talk_user_id=2, message="messageFrom1")
        message.save()
        message2 = Messages(room_name="2T1", user_id=2, talk_user_id=1, message="messageFrom2")
        message2.save()

        url = reverse('login')
        data = {
            'username': 'saigo',
            'password': 'saigo'
        }
        self.response = self.client.post(url, data)

        data = {
            'talkToId': 2
        }
        url = reverse('chat')
        self.response = self.client.post(url, data)

        self.assertEqual(self.response.context.get('user').id, 1)
        self.assertEqual(self.response.context.get('talkTo').id, 2)

        self.response = self.client.get(reverse('logout'))
        url = reverse('login')
        data = {
            'username': 'sato',
            'password': 'sato'
        }
        self.response = self.client.post(url, data)

        data = {
            'talkToId': 1
        }
        url = reverse('chat')
        self.response = self.client.post(url, data)

        self.response = self.client.post(url, data)
        self.assertEqual(self.response.context.get('user').id, 2)
        self.assertEqual(self.response.context.get('talkTo').id, 1)

    def tearDown(self):
        User.objects.all().delete()
        Likes.objects.all().delete()
        Messages.objects.all().delete()


# WebSocketを用いたchatに関連すること及びテストメソッドが非同期である必要があるものをまとめたテストクラス。
class MessageTest(TestCase):
    def setUp(self):

        user = User.objects.create_user('saigo', '', 'saigo')
        user.profile.gender = '男性'
        user.profile.save()

        user2 = User.objects.create_user('sato', '', 'sato')
        user2.profile.gender = '女性'
        user2.profile.save()

        like = Likes(user_id=1, liked_user_id=2)
        like.save()
        like = Likes(user_id=2, liked_user_id=1)
        like.save()

    # Websocket通信として接続・切断できるかをテストするメソッド
    async def test_connect_websocket(self):

        communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "ws/chat/")

        connected, subprotocol = await communicator.connect()

        assert connected
        await communicator.disconnect()

    # WebSocketに対するJSONの送信及びその受信内容の非同期送信が可能であることをテストするメソッド。
    async def test_send_receive_message(self):

        communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "ws/chat/")

        # user_idが1と2であるユーザー同士を同じチャットルームに参加させるためのパラメータ。
        join = {"data_type": "join", "username": "saigo", "roomname": "1T2"}
        connected, subprotocol = await communicator.connect()

        toJson = {"test": "test", "message": "hello", "user_id": "1", "talk_user_id": "2", "room": "1T2"}

        sem = asyncio.Semaphore(100)
        try:
            async with sem:
                with async_timeout.timeout(100):
                    # 2人のユーザーを同じチャットルームに参加させる。
                    await communicator.send_json_to(join)
                    # テストメッセージ送信。
                    await communicator.send_json_to(toJson)

        except Exception as e:
            print('type:' + str(type(e)))
            print('args:' + str(e.args))
            print('e自身:' + str(e))

        sem = asyncio.Semaphore(200)
        try:
            async with sem:
                with async_timeout.timeout(200):
                    # 上での送信内容（WebSocketが送信したもの）を受信。
                    response = await communicator.receive_json_from()
                    assert response == {
                        'message': 'hello',
                        'username': 'saigo',
                        'datetime': str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M'))
                    }

        except Exception as e:
            print('type:' + str(type(e)))
            print('args:' + str(e.args))
            print('e自身:' + str(e))

        await communicator.disconnect()

    # messageが保存されているかテストするメソッド。
    async def test_save_message(self):
        self.assertEquals(await self.message_count(), 0)

        await ChatConsumer._save_message("1T2", "1", "2", "testMessage")

        self.assertEquals(await self.message_count(), 1)

    @sync_to_async
    def message_count(cls):
        return Messages.objects.all().count()

    def tearDown(self):
        User.objects.all().delete()
        Likes.objects.all().delete()
        Messages.objects.all().delete()


# ユーザー情報更新に関係するものをテストするクラス。
class UpdateProfileTest(TestCase):
    def setUp(self):
        user = User.objects.create_user('saigo', '', 'saigo')
        user.profile.gender = '男性'
        user.profile.save()

    # /update/に対する正常なアクセスが可能であることをテストするメソッド。
    def test_update_status_code(self):
        url = reverse('login')
        data = {
            'username': 'saigo',
            'password': 'saigo'
        }
        self.response = self.client.post(url, data)
        updateurl = reverse('update', kwargs={'pk': 1})
        self.response = self.client.get(updateurl)
        self.assertEquals(self.response.status_code, 200)

    # ユーザー情報更新をした際に、DBにおいても変更が反映されていることをテストするメソッド。
    def test_update_whether_chenged(self):
        url = reverse('login')
        data = {
            'username': 'saigo',
            'password': 'saigo'
        }
        self.response = self.client.post(url, data)
        updateurl = reverse('update', kwargs={'pk': 1})
        image2 = SimpleUploadedFile(name='ano.png', content=open("media/ano.png", 'rb').read(), content_type='image/png')
        image3 = SimpleUploadedFile(name='ano.png', content=open("media/ano.png", 'rb').read(), content_type='image/png')
        image4 = SimpleUploadedFile(name='ano.png', content=open("media/ano.png", 'rb').read(), content_type='image/png')
        image5 = SimpleUploadedFile(name='ano.png', content=open("media/ano.png", 'rb').read(), content_type='image/png')
        data = {
            'image2': image2,
            'image3': image3,
            'image4': image4,
            'image5': image5,
            'introduction_text': 'テキストテスト'
        }
        self.response = self.client.post(updateurl, data)

        self.assertNotEquals(str(User.objects.get(id=1).profile.image2), 'noPhoto.png')
        self.assertNotEquals(str(User.objects.get(id=1).profile.image3), 'noPhoto.png')
        self.assertNotEquals(str(User.objects.get(id=1).profile.image4), 'noPhoto.png')
        self.assertNotEquals(str(User.objects.get(id=1).profile.image5), 'noPhoto.png')

        os.remove('media/' + str(User.objects.get(id=1).profile.image2))
        os.remove('media/' + str(User.objects.get(id=1).profile.image3))
        os.remove('media/' + str(User.objects.get(id=1).profile.image4))
        os.remove('media/' + str(User.objects.get(id=1).profile.image5))
        self.assertEquals(User.objects.get(id=1).profile.introduction_text, 'テキストテスト')

    def tearDown(self):
        User.objects.all().delete()
