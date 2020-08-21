from django.db import models

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
    created_at = models.DateTimeField(auto_now_add = True)
    secret_status = models.CharField(choices = STATUS_SET, default = STATUS_SECRET, max_length = 8)

