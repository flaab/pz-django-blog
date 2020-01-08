from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post, Comment, Category, User, Tag, Flatpage
from .forms import CommentForm, SearchForm
from django.db.models import Count
from django.db.models import Q
from django.apps import apps
import json
import urllib

#------------------------------------------

def post_search(request):
    """ Receives a query and posts results """

    form = SearchForm()
    query = None
    context = None 
    object_list = []
    meta_title = None
    meta_description = None

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            meta_title = 'Search results for "'+ query +'"'
            meta_description = 'Search results for "'+ query +'"'
            object_list = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))

    # Page and pagination
    paginator = Paginator(object_list, apps.get_app_config('Blog').pagination)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'blog/post_list.html',
                  {'form': form,
                  'query': query,
                  'meta_title': meta_title,
                  'search_string': '&query='+ query,
                  'meta_description': meta_description,
                  'page': page,
                  'posts': posts})

#------------------------------------------

def post_list(request, category_slug = None, tag_slug = None, author_id = None):
    """ Lists all posts, filtered by category and tag, and paginates the results """

    object_list = Post.published.all()
    category = None
    tag = None 
    author = None
    meta_title = None 
    meta_description = None 
    canonical = None

    # If category given
    if(category_slug):
        category = get_object_or_404(Category, slug = category_slug)
        object_list = object_list.filter(category__in=[category])
        canonical = request.build_absolute_uri(category.get_absolute_url())
        meta_description = category.description
        meta_title = category.name

    # If tag given
    if(tag_slug):
        tag = get_object_or_404(Tag, slug = tag_slug)
        object_list = object_list.filter(tags__in=[tag])
        canonical = request.build_absolute_uri(tag.get_absolute_url())
        meta_description = "Posts tagged with "+ tag.name
        meta_title = tag.name

    # If author given
    if(author_id):
        author = get_object_or_404(User, id = author_id)
        object_list = object_list.filter(author__in=[author])
        canonical = request.build_absolute_uri(author.profile.get_absolute_url())
        meta_title = author.profile
        meta_description = "Posts published by "+ str(author.profile)
        
    # Page and pagination
    paginator = Paginator(object_list, apps.get_app_config('Blog').pagination) 
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post_list.html', {'page': page,
                                                        'posts': posts,
                                                        'meta_title': meta_title,
                                                        'meta_description': meta_description,
                                                        'canonical': canonical,
                                                        'category': category,
                                                        'author': author,
                                                        'tag': tag})

#------------------------------------------

def post_discussion(request, year, month, day, post):
    """ Displays the discussion for a given post """

    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)    
    
    # Recaptcha must be used?
    recaptcha_enabled =  apps.get_app_config('Blog').recaptcha_enabled
    
    # Comment defaults to none
    new_comment = None

    # Comment received via post
    if request.method == 'POST':

        # Instance comment form
        comment_form = CommentForm(data = request.POST)

        # Begin reCAPTCHA validation
        if(recaptcha_enabled): 
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': apps.get_app_config('Blog').recaptcha_secret,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
        else:   # No validation
            result = {'success': True}

        # Form must be valid and recaptcha too
        if(comment_form.is_valid() and result['success']):
            new_comment = comment_form.save(commit = False)
            new_comment.post = post 
            new_comment.save()
    # Not received comment yet
    else:
        comment_form = CommentForm()
    
    # Comments (we need to paginate this time)
    comment_count = Comment.objects.filter(post=post, active=True).count() 
    comments_display = apps.get_app_config('Blog').max_comments_discussion
    object_list = post.comments.filter(active = True).order_by('-created')
    
    # Page and pagination
    paginator = Paginator(object_list, comments_display) 
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        comments = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        comments = paginator.page(paginator.num_pages)

    return render(request, 'blog/post_discussion.html', {'post': post,
                                                              'page': page,
                                                              'comments': comments,
                                                              'comment_count': comment_count,
                                                              'new_comment': new_comment,
                                                              'recaptcha_enabled': recaptcha_enabled,
                                                              'comment_form': comment_form})
    

#------------------------------------------

def flatpage(request, slug):
    """ Displays a flatpage or raises a 404 error """

    page = get_object_or_404(Flatpage, slug = slug, status='published')
    host = request.scheme +"://"+ request.get_host();
    canonical = request.build_absolute_uri(page.get_absolute_url())
    return render(request, 'blog/flatpage.html', {'page': page,
                                                       'host': host, 
                                                       'canonical': canonical})

#------------------------------------------

def post_detail(request, year, month, day, post):
    """ Displays a post or raises a 404 error """

    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)    

    # Comments
    comment_count = Comment.objects.filter(post=post, active=True).count() 
    comments_display = apps.get_app_config('Blog').max_comments_per_post
    comments = post.comments.filter(active = True).order_by('-created')[:comments_display]
    new_comment = None

    # Recaptcha must be used?
    recaptcha_enabled =  apps.get_app_config('Blog').recaptcha_enabled

    # Comment received via post
    if request.method == 'POST':

        # Instance comment form
        comment_form = CommentForm(data = request.POST)

        # Begin reCAPTCHA validation
        if(recaptcha_enabled): 
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': apps.get_app_config('Blog').recaptcha_secret,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
        else:   # No validation
            result = {'success': True}

        # Form must be valid and recaptcha too
        if(comment_form.is_valid() and result['success']):
            new_comment = comment_form.save(commit = False)
            new_comment.post = post 
            new_comment.save()
    # Not received comment yet
    else:
        comment_form = CommentForm()

    # Build canonical
    host = request.scheme +"://"+ request.get_host();
    canonical = request.build_absolute_uri(post.get_absolute_url())

    # Get similar posts
    post_tag_ids = post.tags.values_list('id', flat = True)  # Tag ids for this post
    similar_posts = Post.published.filter(tags__in=post_tag_ids).exclude(id=post.id) # Get all posts with this tag, excluding this
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4] #

    return render(request, 'blog/post_detail.html', {'post': post,
                                                          'comments': comments,
                                                          'comment_count': comment_count,
                                                          'meta_description:': post.meta_description,
                                                          'host': host, 
                                                          'canonical': canonical,
                                                          'new_comment': new_comment,
                                                          'similar_posts': similar_posts,
                                                          'recaptcha_enabled': recaptcha_enabled,
                                                          'comment_form': comment_form})
