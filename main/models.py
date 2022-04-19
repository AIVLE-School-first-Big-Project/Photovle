from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
# 장고유저 기반의 커스텀 유저모델
class User(AbstractUser):
    phone = models.CharField("전화번호", max_length=20, blank=False)
    name = models.CharField("이름", max_length=20, blank=False)
    first_name = None
    last_name = None
    class Meta:
        db_table = 'user'

# 게시판 모델
class Board(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
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

# 댓글 모델
class Reply(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=400)
    rep_date = models.DateTimeField()

    def __str__(self):
        return self.comment
