A wordpress alternative for Django sites. A bootstrapped and full-fledged blog engine that blends into django-admin. It implements markdown posts, multiple authors, categories, tags, markdown flatpages, image galleries, comments with moderation, search engine, related posts, discussion pages, atom rss and sitemaps.

# Requirements

# Installation
Create a directory and clone the project.
```
$ mkdir mysite
$ cd mysite
$ git clone https://github.com/flaab/pz-django-blog.git
```
Create the database and tables of the application.
```
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```
Create a superuser for django-admin.
```
$ python3 manage.py createsuperuser
```
If all went well, run the server.
```
$ python3 manage.py runserver
```
The blog is now available at: http://127.0.0.1:8000.
Use the admin site to add content: http://127.0.0.1:8000/admin. 

# Getting started
