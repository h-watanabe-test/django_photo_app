import boto3
from django.http import JsonResponse
from django.http import HttpResponse
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
    """_summary_

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    return render(request, 'collect_iot_info/top.html')

def logout_view(request):
    """_summary_

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    logout(request)
    return render(request, 'collect_iot_info/logout.html')

# S3 Presigned URL発行API
class S3PresignedURLView(LoginRequiredMixin, View):
    """_summary_

    Args:
        LoginRequiredMixin (_type_): _description_
        View (_type_): _description_
    """
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
    """_summary_

    Args:
        LoginRequiredMixin (_type_): _description_
        ListView (_type_): _description_

    Returns:
        _type_: _description_
    """
    model = UploadRecord
    template_name = 'collect_iot_info/upload_list.html'
    context_object_name = 'uploads'

    def get_queryset(self):
        return UploadRecord.objects.filter(user=self.request.user).order_by('-uploaded_at')

class HealthCheckView(View):
    """_summary_

    Args:
        View (_type_): _description_
    """
    def get(self, request, *args, **kwargs):
        """
        ヘルスチェック用のエンドポイント。
        常に200 OKを返します。
        """
        return HttpResponse("OK", status=200)