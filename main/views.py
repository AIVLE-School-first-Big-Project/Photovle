import random
import string
import hashlib
import requests
import os
from .models import *
from .forms import *
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib import auth, messages
from django.contrib.auth import authenticate, update_session_auth_hash, login as dj_login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage
from Photovle.settings import SOCIAL_OUTH_CONFIG

# from rest_auth.registration.views import 
# Create your views here.
def index(request):
    return render(request, 'index.html')

def home(request):
    print(request.user)
    return render(request, 'home.html')

#######################회원관련################################
# 회원가입 1페이지
def signup1(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        context = {
            'name':name,
            'username':username,
            'phone':phone,
        }
        return render(request, 'signup2.html', context)
        # form = UserForm(request.POST)
        # if form.is_valid():
        #     form.save()
        #     username = form.cleaned_data.get('username')
        #     raw_password = form.cleaned_data.get('password1')
        #     user = authenticate(username=username, password=raw_password)
        #     dj_login(request, user)
        #     return redirect('main:home')
    return render(request, 'signup1.html')
    # if request.user.is_authenticated:
    #     return redirect('main:index')
    #     if request.POST['password1'] == request.POST['password2']:
    #         user = User.objects.create_user(
    #             username = request.POST.get('username'),
    #             password = request.POST.get('password'),
    #             email = request.POST.get('email'),
    #         )
    #         auth.login(request, user)
    #         return redirect('main:board')
    #     return render(request, 'signup.html')
    # return render(request, 'signup.html')
# 회원가입 2페이지
def signup2(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            dj_login(request, user)
            return redirect('main:home')
    else:
        form = UserForm()
    context = {
        'form':form,
    }

    return render(request, 'signup2.html', context)

# 카카오 로그인
def kakao_login(request):
    client_id = SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY']
    redirect_uri = SOCIAL_OUTH_CONFIG['KAKAO_REDIRECT_URI']
    url = f"https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}"
    return redirect(url)

def kakao_callback(request):
    code = request.GET.get('code')
    client_id = SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY']
    redirect_uri = SOCIAL_OUTH_CONFIG['KAKAO_REDIRECT_URI']
    url = f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}'
    token_request = requests.post(url)
    token_json = token_request.json()
    # request.session['access_token'] = token_json['access_token']
    # request.session.modified = True
    # return render(request, 'home.html')
    access_token = token_json.get('access_token')
    profile_request = requests.post(
        'https://kapi.kakao.com/v2/user/me',
        headers={'Authorization':f'Bearer {access_token}'},
    )
    profile_json = profile_request.json()
    kakao_id = profile_json.get('id', None)
    account = profile_json.get('kakao_account')
    email = account.get('email', None)

    if User.objects.filter(username=kakao_id).exists():
        user = User.objects.get(username=kakao_id)
        dj_login(request, user)
        # request.session['user'] = user.username
        return redirect('main:home')
        # form = UserForm(request.POST, instance=user)
        # if form.is_valid():
        #     form.save()
        #     username = form.cleaned_data.get('username')
        #     raw_password = form.cleaned_data.get('password1')
        #     user = authenticate(username=username, password=raw_password)
        # return redirect('main:home')
    else:
        # pw = np.random.randint(10000000, size=1)
        tmp = string.ascii_letters + string.digits
        rs = ""
        for _ in range(12):
            rs += random.choice(tmp)
        print(rs)
        password = hashlib.sha256(rs.encode())
        kakao_account = User(
            username=kakao_id,
            email = email,
            password = password
        )
        kakao_account.save()
        user = User.objects.get(email=email)
        # user = request.user
        # request.session['user'] = user.id
        # user = authenticate(username=user.username, password=user.password)
        # print(user.password)
        dj_login(request, user)
        context = {
            'user':user,
        }
        # return redirect('main:home')
        return render(request, 'addinfo.html', context)

# 소셜로그인 시 추가정보 입력
def addinfo(request, pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        form = AddInfoForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            dj_login(request, user)
            return redirect('main:home')
    else:
        form = AddInfoForm(instance=user)
        context = {
            'form':form,
        }
    return render(request, 'addinfo.html', context)

    # user = request.user
    # if request.method == 'POST':
    #     form = UserUpdateForm(request.POST, instance=user)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('main:mypage')



    # code = request.query_params['code']
    # url = "https://kauth.kakao.com/oauth/token"
    # res = {
    #     'grant_type': 'authorization_code',
    #     'client_id': SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY'],
    #     'redirect_uri': SOCIAL_OUTH_CONFIG['KAKAO_REDIRECT_URI'],
    #     'client_secret': SOCIAL_OUTH_CONFIG['KAKAO_SECRET_KEY'],
    #     'code': code,
    # }
    # headers = {
    #     'content-type': 'application/x-www-form-urlencoded;charset=utf-8'
    # }
    # response = requests.post(url, data=res, headers=headers)
    # tokenJson = response.json()
    # userurl = "https://kapi.kakao.com/v2/user/me"
    # auth = "Bearer "+tokenJson['access_token']
    # header = {
    #     'Authorization': auth,
    #     'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
    # }
    # res = requests.get(userurl, headers=header)
    # kakao_res = json.loads(res.text)
    # kakao = SocialPlatform.objects.get(platform_name='kakao')
    # return Response(res.text)

# 로그아웃
def logout(request):
    auth.logout(request)
    return redirect('main:home')

# 마이페이지
@login_required
def mypage(request):
    user = request.user
    context = {
        'user':user
    }
    return render(request, 'mypage.html', context)

# 유저정보수정
@login_required
def update_user(request):
    user = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('main:mypage')
    else:
        form = UserUpdateForm(instance=user)    
    context = {
        'form':form
    }
    return render(request, 'update_user.html', context)

# 비밀번호변경
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, '변경완료')
            return redirect('main:mypage')
        else:
            messages.error(request, '에러')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form':form
    }
    return render(request, 'change_password.html', context)

# 회원탈퇴
def delete_user(request):
    user = request.user
    user.delete()
    auth.logout(request)
    return redirect('main:home')
   
######################## 게시판 ############################

# 게시판 메인페이지
def board(request):
    # all_boards = Board.objects.all().order_by("-pub_date")
    # paginator = Paginator(all_boards, 5)
    # page = int(request.GET.get('page', 1))
    # board_list = paginator.get_page(page)
    # return render(request, 'board.html', {'title':'게시판', 'board_list':board_list})
    board = Board.objects.all().order_by("-pub_date")
    page = int(request.GET.get('page', 1))
    paginator = Paginator(board, 9)
    page_obj = paginator.get_page(page)
    context={ 
                'page_obj':page_obj,
                'title':'게시판',
                'board':board
        }
    return render(request, 'board.html', context)

# 게시판 상세페이지
def detail(request, pk):    # pk = board_id
    board = get_object_or_404(Board, id=pk)
    reply = Reply.objects.filter(board_id=pk).order_by("-rep_date")
    page = int(request.GET.get('page', 1))
    paginator = Paginator(reply, 2)
    page_obj = paginator.get_page(page)
    reply_form = ReplyForm()
    context = {
        'board':board,
        'reply_form':reply_form,
        'page_obj':page_obj,
        'reply':reply,
        'pk':pk
    }
    return render(request, 'detail.html', context)

# 게시판 글쓰기
def write(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            temp_form = form.save(commit=False)
            temp_form.user = request.user
            temp_form.pub_date = timezone.now()
            temp_form.upload_files = request.FILES.get('upload_files')
            temp_form.save()
            return redirect('main:board')
    else:
        form = BoardForm()
    context = {
        'form':form
    }
    return render(request, 'write.html', context)
    # return render(request, 'write.html')
    
# 게시판에 업로드된 파일 다운로드
def download(request, pk):  # pk = board_id
    board = Board.objects.get(id=pk)

    filepath = os.path.abspath('media/')
    file_name = os.path.basename('media/'+board.upload_files.name)

    fs = FileSystemStorage(filepath)
    response = FileResponse(fs.open(file_name, 'rb'), content_type='application/download')
    response['Content-Disposition'] = 'attachment; filename=%s' % file_name
    return response

# 게시글 수정
@login_required
def update(request, pk):    # pk = board_id
    board = Board.objects.get(id=pk)
    tmp = Board.objects.get(id=pk)
    if request.method == 'POST':
        board.title = request.POST['title']
        board.content = request.POST['content']
        board.user = request.user
        board.pub_date=timezone.now()
        board.upload_files = request.FILES.get('upload_files')
        if board.title == '':
            board.title = tmp.title
        if board.content == '':
            board.content = tmp.content
        if board.upload_files == '':
            board.upload_files = tmp.upload_files
        board.save()
        return redirect('main:detail', pk)
    else:
        context = {
            'board':board,
            'pk':pk
        }
    return render(request, 'update.html', context)
    # if request.method == 'POST':
    #     form = BoardForm(request.POST, instance=board)
    #     if form.is_valid():
    #         temp_form = form.save(commit=False)
    #         temp_form.user = request.user
    #         temp_form.pub_date = timezone.now()
    #         temp_form.upload_files = request.FILES.get('upload_files')
    #         temp_form.save()
    #         return redirect('main:board')
    # else:
    #     form = BoardForm(instance=board)
    #     context = {
    #         'form':form,
    #         'pk':pk
    #     }
    # return render(request, 'update.html', context)
        

# 게시글 삭제
@login_required
def delete(request, pk):    # pk = board_id
    board = Board.objects.get(id=pk)
    board.delete()
    return redirect('main:board')

# 게시글에 댓글작성
@login_required
def create_reply(request, pk):  # pk = board_id
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            temp_form = form.save(commit=False)
            temp_form.board = get_object_or_404(Board, id=pk)
            temp_form.user = request.user
            temp_form.rep_date = timezone.now()
            temp_form.save()
            return redirect('main:detail', pk)
    else:
        form = ReplyForm()
        context = {
            'form': form
        }
    #return render(request, 'create_reply.html', context)
    return HttpResponseRedirect(reverse('main:detail', context))

# 댓글수정
@login_required
def update_reply(request, pk, rep_pk):  # pk = board_id
    reply = Reply.objects.get(id=rep_pk)
    if request.method == 'POST':
        form = ReplyForm(request.POST, instance=reply)
        if form.is_valid():
            temp_form = form.save(commit=False)
            temp_form.rep_date = timezone.now()
            temp_form.save()
            return redirect('main:detail', pk)
    else:
        context = {
            'reply': reply,
            'pk':pk,
        }
    return HttpResponseRedirect(reverse('main:detail', context))

# 댓글삭제
@login_required
def delete_reply(request, pk):  # pk = rep_id
    reply = Reply.objects.get(id=pk)
    pk = reply.board_id
    reply.delete()
    return HttpResponseRedirect(reverse('main:detail', args=(pk,)))



# 나의 게시글
@login_required
def mypost(request):
    board = Board.objects.filter(user=request.user).order_by("-pub_date")
    page = int(request.GET.get('page', 1))
    paginator = Paginator(board, 10)
    page_obj = paginator.get_page(page)
    context={ 
                'page_obj':page_obj,
                'title':'나의 게시글'
        }
    return render(request, 'mypost.html', context)

######################## Canvas ############################
from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import glob
# from .models import ImageMetadata

def canvas(request):
    return render(request, 'canvas.html')


def index2(request):
    return render(request, 'index2.html')


def index3(request):
    return render(request, 'index3.html')

def test(request):
    return render(request, 'test.html')


def osvos(request):
    return render(request, 'osvos.html')
