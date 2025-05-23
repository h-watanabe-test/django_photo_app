import boto3
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.shortcuts import render, redirect
from .models import UploadRecord
import os

# トップページ
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required
def top(request):
    return render(request, 'collect_iot_info/top.html')

def logout_view(request):
    logout(request)
    return render(request, 'collect_iot_info/logout.html')

# S3 Presigned URL発行API
class S3PresignedURLView(LoginRequiredMixin, View):
    def post(self, request):
        s3 = boto3.client('s3')
        file_name = request.POST.get('file_name')
        user_name = request.user.username
        key = f'uploads/{user_name}/{file_name}'
        presigned = s3.generate_presigned_post(
            Bucket=os.environ.get('AWS_STORAGE_BUCKET_NAME'),
            Key=key,
            ExpiresIn=3600
        )
        return JsonResponse(presigned)
    
class UploadRecordListView(LoginRequiredMixin, ListView):
    model = UploadRecord
    template_name = 'collect_iot_info/upload_list.html'
    context_object_name = 'uploads'

    def get_queryset(self):
        return UploadRecord.objects.filter(user=self.request.user).order_by('-uploaded_at')
