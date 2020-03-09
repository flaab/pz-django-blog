from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class BlogConfig(AppConfig):
    
    # Short name for the application, used to get attributes
    label = 'Blog'                                        

    # Name for the application to be included in INSTALLED_APPS
    name = 'blog'                                        

    # App name for the Administration Site
    verbose_name  = "Django Blog"
    
    # Application settings 
    pagination          = 5                                             # Pagination elements
    meta_title          = _('My Blog')                                  # Meta Title
    header_title        = "Django<strong>Blog</strong>"                 # Header Title
    header_description  = _('A reusable blog app developed for Django') # Header Description
    footer              = _('Proudly powered by PZ-Django-Blog')        # Footer message

    # Recaptcha
    recaptcha_enabled   = True
    recaptcha_sitekey   = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI' 
    recaptcha_secret    = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'

    # Comments in post page
    max_comments_per_post = 5

    # Comments in discussion page
    max_comments_discussion = 20

    # Amount of posts in RSS feed
    posts_in_feed = 20