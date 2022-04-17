from cProfile import label
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *

class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    phone = forms.IntegerField(label='전화번호')
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'phone')

class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'content']

class ReplyForm(ModelForm):
    class Meta:
        model = Reply
        fields = ['comment']


    