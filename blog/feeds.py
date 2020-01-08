from django.contrib.syndication.views import Feed 
from django.template.defaultfilters import truncatewords
from django.apps import apps
from .models import Post 

class LatestPostFeed(Feed):
    title = apps.get_app_config('Blog').meta_title
    description = apps.get_app_config('Blog').header_description
    link  = '/blog/'
    
    def items(self):
        posts_in_feed = apps.get_app_config('Blog').posts_in_feed
        return Post.published.all()[:posts_in_feed]

    def item_title(self, item):
        return item.get_meta_title() 
    
    def item_description(self, item):
        return item.get_meta_description()
    
