from django.db import models
from django.utils import timezone

# Create your models here.

class User(models.Model):
    STATUS_SECRET = "secret"
    STATUS_PUBLIC = "public"
    STATUS_SET = (
        (STATUS_SECRET, "鍵垢"),
        (STATUS_PUBLIC, "公開垢")
    )
    user_name = models.CharField(max_length = 50) # 電電
    user_id = models.BigIntegerField() # 1235677
    screen_name = models.CharField(max_length = 50) # yosyuaomenww
    created_at = models.DateTimeField(default=timezone.now)
    secret_status = models.CharField(choices = STATUS_SET, default = STATUS_SECRET, max_length = 8)

    def __repr__(self):
        # 表示を変更
        return "{}: {}".format(self.pk, self.user_name)
    __str__ = __repr__

class Task(models.Model):
    task = models.CharField(max_length = 140)
    created_at = models.DateTimeField(default=timezone.now)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)

    def __repr__(self):
        return "{}:{}".format(self.pk, self.task)
    __str__ = __repr__

class Task_history(models.Model):
    tweet_id = models.BigIntegerField()
    tweet_text = models.CharField(max_length = 140)
    created_at = models.DateTimeField(default=timezone.now)
    praised = models.BooleanField(default = False)
    task_id = models.ForeignKey(Task, on_delete = models.CASCADE)

    def __repr__(self):
        return "{}".format(self.pk)

    