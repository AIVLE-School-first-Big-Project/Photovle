from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name='main'

urlpatterns = [
    # 메인페이지
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    # 로그인, 로그아웃
    path('home/login/', views.login, name='login'),
    path('home/logout/', views.logout, name='logout'),
    # 카카오 소셜로그인
    path('home/login/kakao/', views.kakao_login, name='kakao_login'),
    path('home/login/kakao/callback/', views.kakao_callback, name='kakao_callback'),
    # 회원가입
    path('home/signup/', views.signup, name='signup'),
    path('home/<int:pk>/addinfo/', views.addinfo, name='addinfo'),
    # 마이페이지
    path('home/mypage/', views.mypage, name='mypage'),
    path('home/update_user/', views.update_user, name='update_user'),
    path('home/delete_user/', views.delete_user, name='delete_user'),
    path('home/change_password/', views.change_password, name='change_password'),
    # 게시판
    path('board/', views.board, name='board'),
    path('board/<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/download/', views.download, name='download'),
    path('board/write/', views.write, name='write'),
    path('board/<int:pk>/update', views.update, name='update'),
    path('<int:pk>/delete', views.delete, name='delete'),
    path('mypost/', views.mypost, name='mypost'),
    # 댓글
    path('<int:pk>/create_reply', views.create_reply, name='create_reply'),
    path('<int:pk>/<int:rep_pk>/update_reply/', views.update_reply, name='update_reply'),
    path('<int:pk>/delete_reply', views.delete_reply, name='delete_reply'),
    # 작업Canvas
    path('osvos/', views.osvos, name='osvos'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)