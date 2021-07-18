from datetime import datetime
from django.core.checks import messages
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from .models import BoardModel, Likes, Nopes,Profile, Messages
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.utils import timezone

# Create your views here.

def signupfunc(request):
    object_list = User.objects.all()    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if '-' in username or User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error':'ユーザーネームに無効な文字が含まれているか、既に存在しているユーザーネームです。'})
        try:
            user = User.objects.create_user(username, '', password)
            login(request, user)
            print(user.get_username)
            #後でupdateに変更
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
    # nopeUsers = Nopes.objects.filter(user_id=request.user.id)
    
    object_list = []
    allUsers = User.objects.all()

    print(Likes.objects.filter(user_id=1, liked_user_id=3).exists())

    
    for user in allUsers:
        if not Likes.objects.filter(user_id=request.user.id, liked_user_id=user.id).exists() and not Nopes.objects.filter(user_id=request.user.id ,noped_user_id=user.id).exists() and user.id != request.user.id:
            object_list.append(user)
            break
    
    likeUsers = Likes.objects.filter(user_id=request.user.id)
    likedUsers = Likes.objects.filter(liked_user_id=request.user.id)
    machingFlag = "false"
    machingUser = User.objects.get(id=request.user.id)
    for item in likeUsers:
        for item2 in likedUsers:
            if item.liked_user_id == item2.user_id:
                aaaa = datetime.now()
                if 2 > (aaaa.replace(tzinfo=None)-item.like_date.replace(tzinfo=None)).total_seconds():
                    machingUser = User.objects.get(id=item.user_id)
                    machingFlag = "true"
                    return render(request, 'maching.html', {"machingUser":machingUser})
    if len(object_list) != 0:
        nextUser = object_list[0]
    else:
        nextUser = None
    # return render(request, 'list.html', {'object_list':object_list,"machingFlag":machingFlag})
    return render(request, 'list.html', {'object_list':object_list,"machingUser":machingUser, "nextUser":nextUser})

def logoutfunc(request):
    logout(request)
    return redirect('login')

def detailfunc(request, pk):
    object = get_object_or_404(BoardModel, pk=pk)
    return render(request, 'detail.html', {'object':object})

def goodfunc(request, pk):
    #object = BoardModel.objects.get_object_or_404(BoardModel, pk=pk)
    object = BoardModel.objects.get(pk=pk)
    #object.good += 1
    object.good = object.good + 1
    object.save()
    return redirect('list')

class BoardCreate(CreateView):
    template_name = 'create.html'
    model = BoardModel
    fields = ('title','content','author','snsimage')
    success_url = reverse_lazy('list')

#ここから
@login_required
def likefunc(request, pk):
    #object = BoardModel.objects.get_object_or_404(BoardModel, pk=pk)
    like = Likes(user_id=request.user.id, liked_user_id=pk)
    print(request.user.id)
    #object.good += 1
    # object.user_id = request.user.id
    # object.liked_user_id = pk
    like.save()
    return redirect('list')

@login_required
def nopefunc(request, pk):
    #object = BoardModel.objects.get_object_or_404(BoardModel, pk=pk)
    nope = Nopes(user_id=request.user.id, noped_user_id=pk)
    #object.good += 1
    # object.user_id = request.user.id
    # object.liked_user_id = pk
    nope.save()
    return redirect('list')

@login_required
def deleteMachingfunc(request):
    #object = BoardModel.objects.get_object_or_404(BoardModel, pk=pk)
    print('ログインユーザーidは')
    print(request.user.id)
    print('マッチングユーザーidは')
    print(request.POST['machingUserId'])
    likeUser = Likes.objects.filter(user_id=request.user.id, liked_user_id=request.POST['machingUserId']).delete()

    return redirect('machinglist')

#ここから
@login_required
def machinglistfunc(request):    
    likeUser = Likes.objects.filter(user_id=request.user.id)
    likedUser = Likes.objects.filter(liked_user_id=request.user.id)
    machingList = []

    for item in likeUser:
        for item2 in likedUser:
            if item.liked_user_id == item2.user_id:

                machingList.append(User.objects.get(pk=item.liked_user_id))

    return render(request, 'machinglist.html', {'machingList':machingList})

@login_required
def profileEditfunc(request):
    profile = Profile.objects.get(pk=request.user.id)
    if request.method == "POST":
        user = request.user
        if request.POST.get('name').strip() == "":
            return redirect('profileEdit')
        else:            
            user.username = request.POST.get('name')
            print(request.FILES.get('image'))
            profile.image = request.FILES.get('image')
            profile.introduction_text = request.POST.get('text')
            user.save()
            profile.save()
            edited = "ユーザー情報を更新しました。"
            return render(request,'profileEdit.html', {'edited':edited, 'profile':profile})
            
    return render(request, 'profileEdit.html', {'profile':profile})


class profileUpdate(UpdateView):
    template_name = 'updateProfile.html'
    model = Profile
    fields = ('image','image2','image3','image4','image5','introduction_text')
    # success_url = reverse_lazy('<int:pk>/update/')
    success_url = reverse_lazy('list')

@login_required
def chat( request ):
    #kaneko-tanakaかtanaka-kanekoになってしまうので、後で一意にする処理追加。また、usernameは一意にしてハイフンはダメにする
    # room = request.POST['talkTo'] + "-" + request.user.username
    if request.POST.get('talkToId') == None:
        return redirect('machinglist')
    print("def chatです")
    print(request.POST.get('talkToId'))
    print("def chatです2")
    myId = str(request.user.pk)
    talkToId = str(request.POST['talkToId'])
    
    # talkToId = str(request.POST.get('talkToId'))
    room = "str"
    if myId < talkToId:
        room = myId + "T" + talkToId
    else:
        room = talkToId + "T" + myId
    
    messages = []
    for dbMessage in Messages.objects.filter(room_name=room):
        # print(type(dbMessage.send_date))
        if dbMessage.user_id==request.user.id:
            messageDictionary = {"username":request.user.username,"message":dbMessage.message,"date":str(dbMessage.send_date.strftime( '%Y/%m/%d %H:%M' ))}
            # messageDictionary = {"username":request.user.username,"message":dbMessage.message}
            messages.append(messageDictionary)
        else:
            messageDictionary1 = {"username":User.objects.get(id=talkToId).username,"message":dbMessage.message,"date":str(dbMessage.send_date.strftime( '%Y/%m/%d %H:%M' ))}
            # messageDictionary1 = {"username":User.objects.get(id=talkToId).username,"message":dbMessage.message}
            messages.append(messageDictionary1)
    return render( request, 'chat.html', {'room':room, 'talkTo':User.objects.get(id=talkToId),'user':request.user,'messages':messages})

  