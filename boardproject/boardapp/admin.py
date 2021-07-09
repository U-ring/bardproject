from django.contrib import admin
from .models import BoardModel, Profile

# Register your models here.

admin.site.register(BoardModel)

admin.site.register(Profile)