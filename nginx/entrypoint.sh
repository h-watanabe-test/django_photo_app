#!/bin/bash
set -e

# Djangoアプリのホスト名とポート
DJANGO_HOST="localhost" # 同じタスク内のコンテナはlocalhostで通信可能
DJANGO_PORT="8000"
DJANGO_HEALTH_ENDPOINT="/health" # Djangoアプリのヘルスチェックエンドポイント

echo "Waiting for Django app to be ready..."
until curl --fail -s http://${DJANGO_HOST}:${DJANGO_PORT}${DJANGO_HEALTH_ENDPOINT}; do
    echo "Django app is not yet ready. Waiting..."
    sleep 5
done

echo "Django app is ready. Starting Nginx..."

# Nginxを起動
exec nginx -g "daemon off;"