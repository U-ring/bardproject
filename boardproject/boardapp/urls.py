from django.urls import path
from .views import signupfunc, loginfunc, listfunc, logoutfunc, detailfunc, goodfunc, BoardCreate , profileUpdate, likefunc, nopefunc, machinglistfunc, profileEditfunc, chat
from django.urls import include

urlpatterns = [
    path('signup/', signupfunc, name='signup'),
    path('login/', loginfunc, name='login'),
    path('list/', listfunc, name='list'),
    path('logout/', logoutfunc, name='logout'),
    path('detail/<int:pk>', detailfunc, name='detail'),
    path('good/<int:pk>', goodfunc, name='good'),
    path('create/', BoardCreate.as_view(), name='create'),
    path('like/<int:pk>', likefunc, name='like'),
    path('nope/<int:pk>', nopefunc, name='nope'),
    path('machinglist/', machinglistfunc, name='machinglist'),
    path('profileEdit/', profileEditfunc, name='profileEdit'),
    path('<int:pk>/update/', profileUpdate.as_view(), name='update'),
    path( '', chat, name='chat' ),
    # path( '<int:pk>', chat, name='chat' ),
]


path( '', chat, name='chat' ),