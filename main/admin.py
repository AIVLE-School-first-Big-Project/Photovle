from django.contrib import admin
from .models import Board, Reply, User

# Register your models here.
admin.site.register(Board)
admin.site.register(User)
admin.site.register(Reply)