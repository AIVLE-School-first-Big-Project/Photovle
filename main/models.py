from django.utils import timezone
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    phone = models.CharField("전화번호", max_length=20, blank=True)
    first_name = None
    class Meta:
        db_table = 'user'

class Board(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.TextField(max_length=1000)
    hits = models.PositiveIntegerField(default=0)
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.title
    @property
    def update_counter(self):
        self.hits = self.hits + 1
        self.save()

class Reply(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    comment = models.TextField(max_length=400)
    rep_date = models.DateTimeField()

    def __str__(self):
        return self.comment