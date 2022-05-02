from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf import settings
from . import views

# 라벨링 추가: 강준영
from rest_framework import routers
router = routers.DefaultRouter()

app_name='main'

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
# 회원가입, 로그인
    path('home/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('home/login/kakao/', views.kakao_login, name='kakao_login'),
    path('home/login/kakao/callback/', views.kakao_callback, name='kakao_callback'),
    # path('home/kakao/finish/', views.KakaoLogin.as_view(), name='kakao_login_todjango'),
    path('home/logout/', views.logout, name='logout'),
    path('home/signup1/', views.signup1, name='signup1'),
    path('home/signup2/', views.signup2, name='signup2'),
    path('home/<int:pk>/addinfo/', views.addinfo, name='addinfo'),
    path('home/mypage/', views.mypage, name='mypage'),
    path('home/update_user/', views.update_user, name='update_user'),
    path('home/delete_user/', views.delete_user, name='delete_user'),
    path('home/change_password/', views.change_password, name='change_password'),

# 게시판
    path('board/', views.board, name='board'),
    path('board/<int:pk>/', views.detail, name='detail'),
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
    path('index2/', views.index2, name='index2'),
    path('index3/', views.index3, name='index3'),

# 테스트TEST
    path('test/', views.test, name='test'),
    path('osvos/', views.osvos, name='osvos'),
    
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)