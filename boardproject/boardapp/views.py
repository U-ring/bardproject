from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from .models import BoardModel, Likes, Nopes,Profile
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

# Create your views here.

def signupfunc(request):
    object_list = User.objects.all()    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username, '', password)
            return render(request, 'signup.html', {'some':100})
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
            return render(request, 'login.html', {})
    return render(request, 'login.html', {})
@login_required
def listfunc(request):    
    likeUsers = Likes.objects.filter(user_id=request.user.id)
    nopeUsers = Nopes.objects.filter(user_id=request.user.id)
    object_list = []
    allUsers = User.objects.all()

    for user in allUsers:
        if not Likes.objects.filter(liked_user_id=user.id).exists():
            object_list.append(user)
        for line in object_list:
            for nopeUser in nopeUsers:
                if not Nopes.objects.filter(noped_user_id=user.id).exists() and nopeUser.noped_user_id != line.id:
                    object_list.append(user)

    return render(request, 'list.html', {'object_list':object_list})

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
def likefunc(request, pk):
    #object = BoardModel.objects.get_object_or_404(BoardModel, pk=pk)
    like = Likes(user_id=request.user.id, liked_user_id=pk)
    #object.good += 1
    # object.user_id = request.user.id
    # object.liked_user_id = pk
    like.save()
    return redirect('list')

def nopefunc(request, pk):
    #object = BoardModel.objects.get_object_or_404(BoardModel, pk=pk)
    nope = Nopes(user_id=request.user.id, liked_user_id=pk)
    #object.good += 1
    # object.user_id = request.user.id
    # object.liked_user_id = pk
    nope.save()
    return redirect('list')

#ここから
def machinglistfunc(request):    
    likeUser = Likes.objects.filter(user_id=request.user.id)
    likedUser = Likes.objects.filter(liked_user_id=request.user.id)
    machingList = []

    for item in likeUser:
        for item2 in likedUser:
            if item.liked_user_id == item2.user_id:
                # machingList = User.objects.get(pk=item.liked_user_id)
                machingList.append(User.objects.get(pk=item.liked_user_id))
    return render(request, 'machinglist.html', {'machingList':machingList})

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
    success_url = reverse_lazy('list')

def chat( request ):
    print("通ったよ")
    return render( request, 'chat.html' )