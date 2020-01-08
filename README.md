# A wordpress alternative for Django Sites
A wordpress alternative for Django sites. A bootstrapped and full-fledged blog engine that blends into django-admin. It implements markdown posts and flatpages, multiple authors, categories, tags, galleries, moderated comments with recaptcha, search engine, related posts, discussion pages, social sharing, json-ld schemas, RSS feed and sitemap.

## Requirements
- Python >= 3.0
- Django >= 2.2.6
- Markdown
- Hashlib
- Urllib
- Json

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

## Settings 
If you run the blog as an app in a bigger project, delete the following line from *mysite/urls.py*.
```
path('', include(('blog.urls', 'blogdefault'), namespace = 'blogdefault')),
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

## Todo
- Ability to ban commentators
- Posting ping notifications
- Nested comments
- Theming support
- Contact form
- Newsletter

## Authors
**Arturo Lopez Perez** - Main and sole developer (so far).

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details