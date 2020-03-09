# A wordpress alternative for Django Sites

A bootstrapped and complete blog engine that blends into django-admin and works as desired right out of the box.

![PZ-Django-Blog](https://www.dropbox.com/s/sqoj5n950ei4kv3/pz-django-blog.png?raw=1)

## Features

- Mark-down posts and flatpages
- Multiple authors with bio and avatar
- Moderated comments with gravatars and recaptcha
- internationalization support (i18n)
- Browseable categories and tags
- Embeddable media galleries
- Built-in search engine
- Discussion pages
- Json-ld schemas
- Social sharing
- Related posts
- Atom RSS feed
- Sticky posts
- Sitemap

## What makes it different?

- It is a complete engine that works out of the box
- The templates are bootstrap-ready and fully customizable
- It does not depend on foreign apps

## Requirements
- Python >= 3.0
- Django >= 2.2.6
- Markdown
- Hashlib

## Languages
Gettext files are available for the following languages:

- English
- Spanish
- German (translation pending)
- Italian (translation pending)
- French (translation pending)
- Russian (translation pending)
- Japanese (translation pending)
- Portuguese (translation pending)

Kindly share if you create translations for these languages.

## Installation
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
If all went well, the server is up and running: 

- The blog is available at http://127.0.0.1:8000 and http://127.0.0.1:8000/blog.
- The RSS Feed is available at http://127.0.0.1:8000/blog/feed 
- The sitemap is available at http://127.0.0.1:8000/sitemap.xml 

Use the admin site to add content: http://127.0.0.1:8000/admin. 

## Running the blog in a existing Django Site

The above instructions will create a new Django project that will run the blog. If you did that, you can skip this section. If on the other hand, you want to include the blog in your existing application, then another course of action is needed. Add the following lines in your *settings.py*:

```
# Requirements
from django.contrib.messages import constants as messages
from django.utils.translation import gettext_lazy as 

# Site ID
SITE_ID = 1 

# Apps
INSTALLED_APPS = (
    # ...
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'blog',
)

# Middleware
MIDDLEWARE = [
    # ...
    'django.middleware.locale.LocaleMiddleware',  # Between session and common
    # ...
]

# Internationalization
LANGUAGE_CODE = 'en' # Changed to en from en-us
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGES = (
    ('en', _('English')),
    ('es', _('Spanish')),
    ('de', _('German')),
    ('it', _('Italian')),
    ('fr', _('French')),
    ('ru', _('Russian')),
    ('ja', _('Japanese')),
    ('pt', _('Portuguese')),
)
LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale/'),)

# Static
STATIC_URL = '/static/'

# Media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

# Bootstrap messages tags
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}
```

Add the following lines in your *urls.py*:

```
from blog.sitemaps import PostSiteMap, CategorySiteMap, TagSiteMap
from django.conf.urls.static import static
sitemaps = {
    # ...
    'posts': PostSiteMap,
    'categories': CategorySiteMap,
    'tags': TagSiteMap,
}
urlpatterns = [
    # ...,
    path('blog/', include(('blog.urls', 'blog'), namespace = 'blog')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name = 'django.contrib.settings.views.sitemap'),
]
if(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
```

## Getting started
Point your browser to django-admin: http://127.0.0.1:8000/admin and...

- Create a new user to write posts, with first name, last name, bio and avatar.
- Edit the example.com domain under "sites", setting your own.
- Create the categories of your blog posts.
- Write your first post

## Customize the templates
The templates are organized in three categories: extendable templates, includable templates and page templates. Each uses a different naming convention. The templates the application uses are the following, which you can edit to fit your needs. Stylesheets and Javascript files are hotlinked from cdn repositories but you can place your own under *blog/static/*.

- *templates/blog/__l_base.html* => Base layout for the blog
- *templates/blog/_sideposts.html* => Template tag to display recent and most commented posts
- *templates/blog/_categories.html* => Template tag to display the categories
- *templates/blog/_comment.html* => Includable template to display a comment
- *templates/blog/_comment_form.html* => Includate template to display the comment form
- *templates/blog/_tags.html* => Template tag to display the tags
- *templates/blog/_search_box.html* => Template tag to display the search form
- *templates/blog/flatpage.html* => Page template for flatpages
- *templates/blog/post_discussion.html* => Page template for post discussion.
- *templates/blog/post_list.html* => Page template for the post list
- *templates/blog/post_detail.html* => Page template for post details.
- *templates/_pagination.html* => Includable template to display pagination links.

## To-do
- Translations for german, italian, french, russian, portuguese and japanese
- Ability to ban commentators
- Posting ping notifications
- Archive browsing by year and month
- Nested comments
- Theming support

## Authors
**Arturo Lopez Perez** - Main and sole developer (so far).

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details