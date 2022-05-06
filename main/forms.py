from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django import forms
from .models import Board, Reply, User

# 유저 생성 form
class UserForm(UserCreationForm):
    name = forms.CharField(label='이름')
    email = forms.EmailField(label="이메일")
    phone = forms.CharField(label='전화번호')
    
    class Meta:
        model = User
        fields = ('name', 'username', 'password1', 'password2', 'email', 'phone')

# 소셜로그인 시 추가정보입력 form
class AddInfoForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('name', 'username', 'phone')

# 유저정보 수정 form
class UserUpdateForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('name', 'email', 'phone')

# 게시판 글쓰기 form
class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'content', 'upload_files']

# 게시판 댓글 form
class ReplyForm(ModelForm):
    class Meta:
        model = Reply
        fields = ['comment']
