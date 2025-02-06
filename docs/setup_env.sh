#! /bin/bash 
# install necessary packages for development
pip install -r requirements-dev.txt
git add requirements-dev.txt
git commit -m "setup python virtual environment and install necessary packages specified in requirements-dev.txt"

# create default project structure and settings.
django-admin startproject proj .  
git add proj/ manage.py 
git commit -m "start project with default layout"

# customize project structure and settings
mkdir proj/settings 
mv proj/settings.py proj/settings/base.py 
touch proj/settings/development.py 
touch proj/settings/production.py 

# layout structures for templates, static files, and media files
mkdir  -p templates static/css static/js static/img media 
touch templates/base.html templates/header.html templates/footer.html 

# create apps for the ecommerce system and layout structures for each apps
apps=(index account customer developer vendor product order warehouse api_v1) 
for app in ${apps[@]}
do 
    python manage.py startapp ${app}

    touch ${app}/urls.py
    echo "from django.urls import path" >> ${app}/urls.py
    echo "urlpatterns = []" >> ${app}/urls.py

    rm ${app}/views.py
    mkdir ${app}/views
    touch ${app}/views/__init__.py

    mkdir -p ${app}/templates/${app}
    
    rm ${app}/tests.py
    mkdir ${app}/tests
    touch ${app}/tests/__init__.py
    touch ${app}/tests/setup_data.py
    
done 

# define specific layouts for APIs
mkdir api_v1/serializers
touch api_v1/serializers/__init__.py

for app in ${apps[@]}
do
    touch api_v1/views/${app}.py
    touch api_v1/serializers/${app}.py
done
rm api_v1/views/api_v1.py
rm api_v1/views/index.py
rm api_v1/serializers/api_v1.py
rm api_v1/serializers/index.py

# miscellaneous
mkdir screenshots
# mkdir docs
mkdir logs