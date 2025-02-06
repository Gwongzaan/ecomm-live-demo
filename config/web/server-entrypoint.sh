#!/bin/sh

until cd $APP_HOME
do
    echo "Waiting for server volume..."
done

python manage.py collectstatic --noinput

until python manage.py makemigrations
do
    echo "Waiting for makemigrations"
done

until python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 60
done

cat << EOF | python manage.py shell
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.filter(username='live_demo').exists() or User.objects.create_superuser('live_demo', 'live_demo@gwongzaanmok.com', 'live_demo123456789')

EOF


#echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='mog').exists() User.objects.create_superuser('mog', 'mog@sixdigit.net', '93k67y87S70T')" | python manage.py shell \
gunicorn proj.wsgi --bind 0.0.0.0:8000 --workers 4 --threads 4 --reload