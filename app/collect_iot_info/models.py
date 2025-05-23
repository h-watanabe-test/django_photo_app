from django.db import models
from django.contrib.auth.models import User

class UploadRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    s3_key = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)   # 送信日時
    updated_at = models.DateTimeField(auto_now=True)        # 更新日時（保存時刻）
    image_url = models.URLField()                           # S3画像URL