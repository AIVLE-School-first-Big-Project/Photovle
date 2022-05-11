import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from Photovle import settings

# Create your models here.
# 장고유저 기반의 커스텀 유저모델
'''
장고에서 제공하는 auth를 확장하여 사용
phone : 유저의 전화번호(동일한 번호로 가입불가)
name : 유저의 이름
email : 유저의 이메일(동일한 이메일로 가입불가, 비밀번호초기화를 위해 입력받음)
'''
class User(AbstractUser):
    phone = models.CharField("전화번호", max_length=11, unique=True)
    name = models.CharField("이름", max_length=20)
    email = models.EmailField("이메일", max_length=200, unique=True)
    first_name = None
    last_name = None
    
    class Meta:
        db_table = 'user'

# 게시판 모델
'''
title : 게시글 제목
user : 게시글을 작성하는 유저
content : 게시글 내용
hits : 게시글의 조회수
pub_date : 게시글을 작성한 시간 or 수정한 시간
upload_files : 게시글에 첨부한 파일
'''
class Board(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    hits = models.PositiveIntegerField(default=0)
    pub_date = models.DateTimeField()
    upload_files = models.FileField(upload_to="", null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def update_counter(self):
        self.hits = self.hits + 1
        self.save()
        
    def delete(self, *args, **kwargs):
        if self.upload_files:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.upload_files.path))
        super(Board, self).delete(*args, **kwargs)

# 댓글 모델
'''
board : 댓글이 달리는 board_id
user : 댓글을 다는 user_id
comment : 댓글내용
rep_date : 댓글을 작성한 시간 or 수정한 시간
'''
class Reply(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=400)
    rep_date = models.DateTimeField()

    def __str__(self):
        return self.comment
