from django.urls import path
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf import settings
from . import views

app_name='main'

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
# 회원가입, 로그인
    path('home/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('home/logout/', views.logout, name='logout'),
    path('home/signup/', views.signup, name='signup'),
    path('home/mypage/', views.mypage, name='mypage'),
    path('home/update_user/', views.update_user, name='update_user'),
    path('home/delete_user/', views.delete_user, name='delete_user'),
    path('home/change_password/', views.change_password, name='change_password'),

# 게시판
    path('board/', views.board, name='board'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/download/', views.download, name='download'),
    path('write/', views.write, name='write'),
    # path('write/write_board', views.write_board, name='write_board'),
    path('<int:pk>/update', views.update, name='update'),
    path('<int:pk>/delete', views.delete, name='delete'),
    path('mypost/', views.mypost, name='mypost'),
# 댓글
    path('<int:pk>/create_reply', views.create_reply, name='create_reply'),
    path('<int:pk>/<int:rep_pk>/update_reply/', views.update_reply, name='update_reply'),
    path('<int:pk>/delete_reply', views.delete_reply, name='delete_reply'),
# 작업Canvas
    path('canvas/', views.canvas, name='canvas'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)