from django.contrib.auth.models import update_last_login
from django.urls import path
from .views import signupfunc, loginfunc, listfunc, logoutfunc, detailfunc, goodfunc, BoardCreate , likefunc, nopefunc, machinglistfunc, profileEditfunc, profileUpdate
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
]