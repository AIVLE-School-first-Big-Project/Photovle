from django.conf import settings
from django.db import models
# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
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
    board_num = models.ForeignKey(Board, on_delete=models.CASCADE, null=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    comment = models.TextField(max_length=400)
    rep_date = models.DateTimeField()

    def __str__(self):
        return self.comment