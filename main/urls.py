from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

app_name='main'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('index/', views.index, name='index'),
    path('home/', views.home, name='home'),

    path('board/', views.board, name='board'),
    path('<int:id>/', views.detail, name='detail'),
    path('write/', views.write, name='write'),
    path('write/write_board', views.write_board, name='write_board'),

    path('<int:id>/update', views.update, name='update'),
    path('<int:id>/delete', views.delete, name='delete'),
    path('<int:id>/create_reply', views.create_reply, name='create_reply'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)