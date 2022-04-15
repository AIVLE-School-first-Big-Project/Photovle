from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Board
from .forms import UserForm
from django.contrib.auth.decorators import login_required
 
# Create your views here.
def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/home')
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form})

def home(request):
    return render(request, 'home.html')

def board(request):
    all_boards = Board.objects.all().order_by("-pub_date")
    paginator = Paginator(all_boards, 5)
    page = int(request.GET.get('page', 1))
    board_list = paginator.get_page(page)
    return render(request, 'board.html', {'title':'게시판', 'board_list':board_list})

def detail(request, id):
    board = Board.objects.get(id=id)
    return render(request, 'detail.html', {'board': board})

def write(request):
    return render(request, 'write.html')

def write_board(request):
    b = Board(title=request.POST['title'], content=request.POST['detail'], pub_date=timezone.now())
    b.save()
    return HttpResponseRedirect(reverse('main:board'))
    
@login_required
def update(request, id):
    b = Board.objects.get(id=id)
    if request.method == "POST":
        b.title=request.POST['title']
        b.content=request.POST['detail']
        b.pub_date=timezone.now()
        if b.title !="":
            b.save()
        return HttpResponseRedirect(reverse('main:detail', args=(id,)))
    else:
        b=Board
        return render(request, 'update.html', {'board':b})

def delete(request, id):
    b = Board.objects.get(id=id)
    b.delete()
    return redirect('main:board')

def create_reply(request, id):
    b = Board.objects.get(id=id)
    b.reply_set.create(comment=request.POST['comment'], rep_date=timezone.now())
    return HttpResponseRedirect(reverse('main:detail', args=(id,)))