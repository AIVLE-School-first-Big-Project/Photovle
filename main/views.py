from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib import auth, messages
from django.contrib.auth import authenticate, update_session_auth_hash, login as dj_login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from fsspec import filesystem
from .models import *
from .forms import *
import os
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage
from django.core.mail.message import EmailMessage


# Create your views here.
def index(request):
    return render(request, 'index.html')

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
            return redirect('main:board')
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form':form})
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
    paginator = Paginator(board, 5)
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
    reply_form = ReplyForm()
    context = {
        'board':board,
        'reply_form':reply_form,
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
    # b = Board.objects.get(id=id)
    # tmp = Board.objects.get(id=id)
    # if request.method == "POST":
    #     b.title=request.POST['title']
    #     b.content=request.POST['detail']
    #     b.pub_date=timezone.now()
    #     if b.title =="":
    #         b.title = tmp.title
    #         b.save()
    #     elif b.content =="":
    #         b.content = tmp.content
    #         b.save()
    #     else:
    #         b.save()
    #     return HttpResponseRedirect(reverse('main:detail', args=(id,)))
    # else:
    #     b=Board
    #     return render(request, 'update.html', {'board':b})
    board = Board.objects.get(id=pk)
    tmp = Board.objects.get(id=pk)
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
    #     form = BoardForm()
    # context = {
    #     'form':form,
    #     'pk':pk
    # }
    # return render(request, 'update.html', context)
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
        form = BoardForm
    context = {
        'form':form,
        'pk':pk
    }
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
        form = ReplyForm(instance=reply)
        context = {
            'form': form
        }
    return render(request, 'create_reply.html', context)

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

def canvas(request):
    return render(request, 'canvas.html')

def index2(request):
    return render(request, 'index2.html')