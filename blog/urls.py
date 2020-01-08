from django.conf.urls import url
from django.urls import path
from .feeds import LatestPostFeed
from . import views

# App name
app_name = 'blog'

# Url Patterns
urlpatterns = [

    # Default lists all posts
    url('^$', views.post_list, name='post_list'),
    
    # List post by category
    path('category/<slug:category_slug>/', views.post_list, name = 'post_list_by_category'),
    
    # List post by tag
    path('tag/<slug:tag_slug>/', views.post_list, name = 'post_list_by_tag'),
    
    # List post by author
    path('author/<int:author_id>/', views.post_list, name = 'post_list_by_author'),

    # Read a post
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name = 'post_detail'),
    
    # Discussion
    path('discussion/<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_discussion, name = 'post_discussion'),
    
    # Flatpage
    path('flatpage/<slug:slug>/', views.flatpage, name = 'flatpage'),

    # Search 
    path('search/', views.post_search, name = 'post_search'),

    # RSS Feed
    path('feed/', LatestPostFeed(), name = 'post_feed')
]
