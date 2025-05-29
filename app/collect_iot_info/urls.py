from django.contrib.auth import views as auth_views
from django.urls import path
from .views import S3PresignedURLView, UploadRecordListView, top, logout_view
from .views import HealthCheckView
from . import views  # 自作の画面表示用ビュー
from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [
    path('get-presigned-url/', S3PresignedURLView.as_view(), name='get_presigned_url'),
    path('uploads/', UploadRecordListView.as_view(), name='upload_list'),
    path('', auth_views.LoginView.as_view(template_name='collect_iot_info/login.html'), name='login'),  # / でログイン
    path('top/', top, name='top'),  # /top/ でトップページ
    path('logout/', logout_view, name='logout'),  # /logout/ でログアウト画面

]
