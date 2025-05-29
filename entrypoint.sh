#!/bin/bash

# エラーが発生したらスクリプトを終了
set -e

echo "Running database migrations..."
# manage.pyの場所を正確に指定する必要がある場合があります
# Djangoプロジェクトのルートディレクトリが /app なので、manage.pyは /app/manage.py になります。
python manage.py migrate --noinput

echo "Migrations completed. Starting Gunicorn..."
# Gunicornを起動
# exec を使用すると、bashプロセスをGunicornプロセスに置き換え、シグナルハンドリングを適切に行える
exec gunicorn myproject.wsgi:application --bind 0.0.0.0:8000