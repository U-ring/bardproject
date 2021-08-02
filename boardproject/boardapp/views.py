from datetime import datetime
from django.core.checks import messages
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from .models import BoardModel, Likes, Nopes, Profile, Messages, GetUser
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse
from django.utils import timezone

# Create your views here.


def signupfunc(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if '-' in username or User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'ユーザーネームに無効な文字が含まれているか、既に存在しているユーザーネームです。'})
        try:
            user = User.objects.create_user(username, '', password)
            user.profile.gender = request.POST['gender']
            user.profile.birth_date = request.POST['birth_date']
            user.profile.save()
            login(request, user)

            # 後でupdateに変更
            return redirect('list')
        except IntegrityError:
            return render(request, 'signup.html', {'error':'このユーザーは既に登録されています。'})
    return render(request, 'signup.html')


def loginfunc(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            return render(request, 'login.html', {"context":"ユーザー名かパスワードを間違えています。"})
    return render(request, 'login.html', {})


@login_required
def listfunc(request):
    loginUser = request.user

    matchingUser = Likes.judgeMatching(loginUser)
    if matchingUser is not None:
        return render(request, 'matching.html', {"matchingUser": matchingUser})

    return render(request, 'list.html', {"nextUser": GetUser.getHeterosexual(loginUser)})


def logoutfunc(request):
    logout(request)
    return redirect('login')


def detailfunc(request, pk):
    object = get_object_or_404(BoardModel, pk=pk)
    return render(request, 'detail.html', {'object': object})


def goodfunc(request, pk):
    object = BoardModel.objects.get(pk=pk)

    object.good = object.good + 1
    object.save()
    return redirect('list')


class BoardCreate(CreateView):
    template_name = 'create.html'
    model = BoardModel
    fields = ('title', 'content', 'author', 'snsimage')
    success_url = reverse_lazy('list')


# ここから
@login_required
def likefunc(request, pk):
    like = Likes(user_id=request.user.id, liked_user_id=pk)
    like.save()
    return redirect('list')


@login_required
def nopefunc(request, pk):

    nope = Nopes(user_id=request.user.id, noped_user_id=pk)

    nope.save()
    return redirect('list')


@login_required
def deleteMatchingfunc(request):
    Likes.objects.filter(user_id=request.user.id, liked_user_id=request.POST['matchingUserId']).delete()

    return redirect('matchinglist')


# ここから
@login_required
def matchinglistfunc(request):

    return render(request, 'matchinglist.html', {'matchingList': Likes.getMatchingUser(request.user)})


class profileUpdate(UpdateView):
    template_name = 'updateProfile.html'
    model = Profile
    fields = ('image', 'image2', 'image3', 'image4', 'image5', 'introduction_text')

    def get_success_url(self):
        return reverse('update', kwargs={'pk': self.object.pk})


@login_required
def chat(request):
    if request.POST.get('talkToId') is None:
        return redirect('matchinglist')
    loginUser = request.user
    myId = str(loginUser.pk)
    talkToId = str(request.POST['talkToId'])

    room = "str"
    if myId < talkToId:
        room = myId + "T" + talkToId
    else:
        room = talkToId + "T" + myId

    return render(request, 'chat.html', {'room': room, 'talkTo': User.objects.get(id=talkToId), 'user': request.user, 'messages': Messages.getMessage(loginUser, talkToId, room)})
