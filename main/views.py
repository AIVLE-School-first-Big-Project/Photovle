from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import auth, messages
from django.contrib.auth import authenticate, update_session_auth_hash, login as dj_login
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, AuthenticationForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, FileResponse
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from Photovle import settings
from Photovle.settings import SOCIAL_OUTH_CONFIG
from .models import User, Board, Reply
from .forms import UserForm, AddInfoForm, UserUpdateForm, ReplyForm, BoardForm
import random
import string
import hashlib
import requests
import os

# Create your views here.
# 로고만 있는 인덱스 페이지
def index(request):
    return render(request, 'index.html')

# 메인페이지
def home(request):
    return render(request, 'home.html')

#######################회원관련################################
# 회원가입
def signup(request):
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
    return render(request, 'signup.html', context)

# 로그인
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            dj_login(request, form.get_user())
            return redirect('main:home')
    else:
        # 로그인 된 유저의 경우 로그인 페이지 접근 불가
        if request.user.is_authenticated:
            return redirect('main:home')
        form = AuthenticationForm()
    context = {
        'form':form,
    }
    return render(request, 'login.html', context)

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
    access_token = token_json.get('access_token')
    profile_request = requests.post(
        'https://kapi.kakao.com/v2/user/me',
        headers={'Authorization':f'Bearer {access_token}'},
    )
    profile_json = profile_request.json()
    kakao_id = profile_json.get('id', None)
    account = profile_json.get('kakao_account')
    email = account.get('email', None)

    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        if user.name=="" or user.phone=="":
            user.delete()
            return redirect('main:login')
        else:
            dj_login(request, user, 'django.contrib.auth.backends.ModelBackend')
            return redirect('main:home')
    else:
        # user 테이블에 넣기 위하여 임의의 password를 만들고 sha256으로 암호화
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
        dj_login(request, user, 'django.contrib.auth.backends.ModelBackend')
        context = {
            'user':user,
        }
        return render(request, 'addinfo.html', context)

# 소셜로그인 시 추가정보 입력
def addinfo(request, pk):   # pk = user_id
    user = User.objects.get(id=pk)    
    if request.method == 'POST':
        form = AddInfoForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            dj_login(request, user, 'django.contrib.auth.backends.ModelBackend')
            return redirect('main:home')
        else:
            user.delete()
            return redirect('main:login')
    else:
        form = AddInfoForm(instance=user)
        context = {
            'form':form,
        }
    return render(request, 'addinfo.html', context)

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

# 비밀번호 초기화
class UserPasswordResetView(PasswordResetView):
    template_name='registration/password_reset_form.html'
    success_url=reverse_lazy('password_reset_done')
    form_class= PasswordResetForm

    def form_valid(self, form):
        if User.objects.filter(email=self.request.POST.get("email")).exists():
            return super().form_valid(form)
        else:
            return render(self.request, 'registration/password_reset_done_fail.html')

# 회원탈퇴
def delete_user(request):
    user = request.user
    user.delete()
    auth.logout(request)
    return redirect('main:home')

#######################게시판################################
# 게시판 메인페이지
def board(request):
    board = Board.objects.all().order_by("-pub_date")
    page = int(request.GET.get('page', 1))
    paginator = Paginator(board, 7)
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
    paginator = Paginator(reply, 5)
    page_obj = paginator.get_page(page)
    context = {
        'board':board,
        'page_obj':page_obj,
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
        if request.FILES:
            if board.upload_files != "":
                os.remove(os.path.join(settings.MEDIA_ROOT, board.upload_files.path))
            board.upload_files = request.FILES.get('upload_files')
        if board.title == '':
            board.title = tmp.title
        if board.content == '':
            board.content = tmp.content
        board.save()
        return redirect('main:detail', pk)
    else:
        context = {
            'board':board,
            'pk':pk,
        }
        if board.upload_files:
            context['file_url'] = board.upload_files.url
    return render(request, 'update.html', context)        

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
    return HttpResponseRedirect(reverse('main:detail', context))

# 댓글수정
@login_required
def update_reply(request, pk, rep_pk):  # pk = board_id # rep_pk = reply_id
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
            'pk':pk,
            'reply': reply,
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
    paginator = Paginator(board, 7)
    page_obj = paginator.get_page(page)
    context={ 
                'page_obj':page_obj,
                'title':'나의 게시글'
        }
    return render(request, 'mypost.html', context)

#######################Canvas################################
def osvos(request):
    return render(request, 'osvos.html')