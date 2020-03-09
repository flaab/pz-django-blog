from django import template
from ..models import Post, Category, Tag
from django.db.models import Count 
from ..forms import CommentForm, SearchForm
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.apps import apps
import markdown

# Register
register = template.Library()

@register.filter(name = 'markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text, extensions=['nl2br']))

@register.simple_tag
def total_posts():
    """ Returns total posts """
    return Post.published.count()

@register.simple_tag
def app_attr(name):
    return(mark_safe(getattr(apps.get_app_config('Blog'), name)))

@register.inclusion_tag('blog/_categories.html')
def show_categories():
    categories = Category.objects.annotate(post_count=Count("blog_posts")).filter(post_count__gt=0).order_by('-post_count','name') 
    #categories = Category.objects.annotate(post_count=Count("blog_posts")).filter(post_count__gt=0).order_by('name')
    # categories = Category.objects.all().order_by('name')
    return{'categories': categories}

@register.inclusion_tag('blog/_tags.html')
def show_tags():
    tags = Tag.objects.annotate(post_count=Count("tags")).filter(post_count__gt=0).order_by('-post_count','name')
    return{'tags': tags}

@register.inclusion_tag('blog/_search_box.html')
def search_box():
    form = SearchForm()
    return{'form': form}

@register.inclusion_tag('blog/_sideposts.html')
def show_latest_posts(count = 5, group_name = _('Recent posts')):
    post_list = Post.published.order_by('-publish')[:count]
    return{'post_list': post_list, 'group_name': group_name}

@register.inclusion_tag('blog/_sideposts.html')
def show_commented_posts(count = 5, group_name = _('Most commented')):
    post_list =  Post.published.annotate(total_comments = Count('comments')).order_by('-total_comments')[:count]
    return{'post_list': post_list, 'group_name': group_name}
