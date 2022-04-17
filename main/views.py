from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView, ListView
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login as dj_login
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')

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
def logout(request):
    auth.logout(request)
    return redirect('main:home')

######################## 게시판 ############################
def board(request):
    # all_boards = Board.objects.all().order_by("-pub_date")
    # paginator = Paginator(all_boards, 5)
    # page = int(request.GET.get('page', 1))
    # board_list = paginator.get_page(page)
    # return render(request, 'board.html', {'title':'게시판', 'board_list':board_list})
    board = Board.objects.all().order_by("-pub_date")
    page = int(request.GET.get('page', 1))
    paginator = Paginator(board, 10)
    page_obj = paginator.get_page(page)
    context={ 
                 'page_obj':page_obj,
                 'title':'게시판'
        }
    return render(request, 'board.html', context)

def detail(request, pk):
    board = get_object_or_404(Board, id=pk)
    reply_form = ReplyForm()
    context = {
        'board':board,
        'reply_form':reply_form,
    }
    return render(request, 'detail.html', context)

def write(request):
    boardForm = BoardForm
    board = Board.objects.all()
    context = {
        'boardForm':boardForm,
        'board':board,
    }
    return render(request, 'write.html', context)
    # return render(request, 'write.html')

def write_board(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        user = request.user
        
        board = Board(
            title = title,
            content = content,
            user = user,
            pub_date=timezone.now()
        )
        board.save()
        return redirect('main:board')

def update(request, pk):
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
    if request.method == 'POST':
        board.title = request.POST['title']
        board.content = request.POST['content']
        board.user = request.user
        board.pub_date=timezone.now()
        board.save()
        return redirect('main:board')
    else:
        boardForm = BoardForm
        return render(request, 'update.html', {'boardForm':boardForm})


def delete(request, pk):
    board = Board.objects.get(id=pk)
    board.delete()
    return redirect('main:board')

def create_reply(request, pk):
    reply_form = ReplyForm(request.POST)
    if reply_form.is_valid():
        temp_form = reply_form.save(commit=False)
        temp_form.board = get_object_or_404(Board, id=pk)
        temp_form.user = request.user
        temp_form.rep_date = timezone.now()
        temp_form.save()
    return HttpResponseRedirect(reverse('main:detail', args=(pk,)))

def delete_reply(request, pk):
    reply = Reply.objects.get(id=pk)
    pk = reply.board_id
    reply.delete()
    return HttpResponseRedirect(reverse('main:detail', args=(pk,)))