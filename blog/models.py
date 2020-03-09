from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.dispatch import receiver
from django.urls import reverse
from django.utils.html import strip_tags
from django.conf import settings
from django import forms
import hashlib

#----------------------------------------

class Profile(models.Model):
    """ User profile to extend the user model with bio and avatar """
    user = models.OneToOneField(User, on_delete = models.CASCADE, verbose_name = _('User'))
    bio = models.TextField(max_length=500, blank = True, null = True, help_text = _('Public bio for the Blog'))
    avatar = models.ImageField(upload_to ='profile/%Y/%m/%d/', blank = True, null = True, 
                               help_text = _('Please upload an squared image'))

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
    
    def get_avatar(self):
        """ Returns the avatar for this user or the gravatar url """
        if not self.avatar:
            return(self.gravatar_url())
        else:
            l_avatar = self.avatar
            return(settings.MEDIA_URL + str(l_avatar))

    def gravatar_url(self):
        """ Gets the URL for the gravatar for this user, used if no native avatar """
        md5 = hashlib.md5(self.user.email.encode())
        digest = md5.hexdigest()
        return('http://www.gravatar.com/avatar/{}'.format(digest))

    def __str__(self): 
        """ Returns a string representation of this user for the blog """
        """ If no first and last name is provided, username is displayed """
        if(self.user.first_name and self.user.last_name):
            return(self.user.first_name +" "+ self.user.last_name)
        else:
            return self.user.username
    
    def get_absolute_url(self):
        return reverse('blog:post_list_by_author', args=[str(self.user.id),])
    

# Signal to delete avatar on profile deletion
@receiver(post_delete, sender = Profile)
def delete_user_profile(sender, instance, **kwargs):
    """ Deletes media objects on deletion of this model """
    instance.avatar.delete(False)  

# Signal to sync profile to user on sql transactions
@receiver(post_save, sender = User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)
    instance.profile.save()

#----------------------------------------

class Category(models.Model):
    """ Categories """

    name = models.CharField(max_length = 80, verbose_name = _('Name'), help_text=_('Enter a descriptive and unique category name'))
    slug = models.SlugField(max_length = 250, help_text=_('The slug is used to link category pages'))
    description = models.TextField(null = True, blank = True, verbose_name = _('Description'), 
                                    help_text=_("Describe what readers can find in this category"))
    created = models.DateTimeField(auto_now_add = True, verbose_name = _('Created')) 
    updated = models.DateTimeField(auto_now = True, verbose_name = _('Updated'))
    
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ('created',)
    
    def get_post_count(self):
        """ Returns amount of posts of this category """
        post_count = Post.objects.filter(category = self).count()
        return(post_count)
    
    def get_absolute_url(self):
        return reverse('blog:post_list_by_category', args=[self.slug,])

    def __str__(self):
        return(self.name)

#----------------------------------------

class Tag(models.Model):
    """ Tags """

    name = models.CharField(max_length = 80, help_text = _('Enter a descriptive tag name'), verbose_name = _('Name'))
    slug = models.SlugField(max_length = 250, help_text = _('The slug is used to link to tag pages'))
    created = models.DateTimeField(auto_now_add = True, verbose_name = _('Created')) 
    updated = models.DateTimeField(auto_now = True, verbose_name = _('Updated'))
    
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        ordering = ('created',)
    
    def get_absolute_url(self):
        return reverse('blog:post_list_by_tag', args=[self.slug,])

    def __str__(self):
        return(self.name)

    def save(self, *args, **kwargs):
        """ Catch save method to replace spaces and go lowercase """
        self.name = self.name.lower()
        self.name = self.name.replace(' ','-')
        return super(Tag, self).save(*args, **kwargs)

#----------------------------------------

class PhotoGallery(models.Model):
    """ A photo gallery can have up to ten images """

    title    = models.CharField(max_length = 250, verbose_name = _('Title'), 
                                                  help_text = _('A clear name facilitates usage of the gallery in other posts'))
    image1   = models.ImageField(upload_to ='gallery/%Y/%m/%d/', help_text = _('At least two images are mandatory to create a gallery.'))
    image2   = models.ImageField(upload_to ='gallery/%Y/%m/%d/', help_text = _('At least two images are mandatory to create a gallery.'))
    image3   = models.ImageField(upload_to ='gallery/%Y/%m/%d/', blank = True, null = True)
    image4   = models.ImageField(upload_to ='gallery/%Y/%m/%d/', blank = True, null = True)
    image5   = models.ImageField(upload_to ='gallery/%Y/%m/%d/', blank = True, null = True)
    image6   = models.ImageField(upload_to ='gallery/%Y/%m/%d/', blank = True, null = True)
    image7   = models.ImageField(upload_to ='gallery/%Y/%m/%d/', blank = True, null = True)
    image8   = models.ImageField(upload_to ='gallery/%Y/%m/%d/', blank = True, null = True)
    image9   = models.ImageField(upload_to ='gallery/%Y/%m/%d/', blank = True, null = True)
    image10  = models.ImageField(upload_to ='gallery/%Y/%m/%d/', blank = True, null = True)
    created = models.DateTimeField(auto_now_add = True, verbose_name = _('Created')) 
    updated = models.DateTimeField(auto_now = True, verbose_name = _('Updated'))
    
    class Meta:
        ordering = ('-created',)
        verbose_name = _('Photo Gallery')
        verbose_name_plural = _('Photo Galleries')

    def get_all_images(self):
        """ Returns all images of this gallery ready to be src """
        images = []
        for field in self._meta.get_fields():
            if(type(field).__name__ == 'ImageField'):
                content = getattr(self, str(field.name)) 
                if(content):
                    images.append(content)
        return(images)

    def __str__(self):
        if(self.title):
            return self.title
        else:
            return _('Gallery created on ')+ created

# Delete gallery files on deletion
@receiver(post_delete, sender = PhotoGallery)
def delete_photogallery_images(sender, instance, **kwargs):
    """ Deletes media objects on deletion of this model """
    instance.image1.delete(False)  
    instance.image2.delete(False)  
    instance.image3.delete(False)  
    instance.image4.delete(False)  
    instance.image5.delete(False)  
    instance.image6.delete(False)  
    instance.image7.delete(False)  
    instance.image8.delete(False)  
    instance.image9.delete(False)  
    instance.image10.delete(False)  

#----------------------------------------

class PublishedManager(models.Manager):
    """ Handles published articles """
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published').order_by('-sticky','-created')

class Post(models.Model):
    """ Blog posts """
    
    STATUS_CHOICES = (
        ('draft', _('Draft')),
        ('published', _('Published')),
    )
    
    author = models.ForeignKey(User, related_name = 'blog_posts', on_delete = models.CASCADE, verbose_name = _('Author'))
    category = models.ForeignKey(Category, related_name = 'blog_posts', on_delete = models.CASCADE, verbose_name = _('Category'))
    title = models.CharField(max_length=250, verbose_name = _('Title'))
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    meta_title = models.CharField(max_length = 250, blank = True, null = True, 
                                  verbose_name = 'Meta title', 
                                  help_text = _("Optional SEO meta-title for this post"))
    meta_description = models.CharField(max_length = 250, blank = True, null = True, 
                                        verbose_name = 'Meta description', 
                                        help_text = _("Optional SEO meta-description for this post"))
    body = models.TextField(verbose_name = _('Body'), 
                            help_text = _("Type the post using plain text/mark-down format and don't use H1 headers"))
    tags = models.ManyToManyField(Tag, related_name="tags", verbose_name = _('tags'))
    cover_image = models.ImageField(upload_to ='blog/%Y/%m/%d/', blank = True, null = True, verbose_name = _('Cover image'))
    gallery = models.ForeignKey(PhotoGallery, related_name = 'blog_posts', on_delete = models.CASCADE, blank = True, null = True,
                                verbose_name = _('Gallery'), help_text = _("Create or link a photo gallery"))
    publish = models.DateTimeField(default=timezone.now, verbose_name=_('Published'))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name = _('Status'))
    comments_enabled = models.BooleanField(default = False, 
                                           verbose_name = _('Comments'), 
                                           help_text = _("Enable or disable public comments for this post"))
    sticky = models.BooleanField(default = False, verbose_name = _('Sticky'), 
                                                  help_text = _("Sticky posts are listed above all others regardless of date"))
    created = models.DateTimeField(auto_now_add = True, verbose_name = _('Created')) 
    updated = models.DateTimeField(auto_now = True, verbose_name = _('Updated'))

    # Our managers
    objects = models.Manager() # The default manager.
    published = PublishedManager() # The Dahl-specific manager.

    def get_meta_title(self):
        """ Returns the meta title if defined. Else the post title. """
        if(self.meta_title):
            return(self.meta_title)
        return(self.title)
    
    def get_meta_description(self):
        """ Returns the meta description if defined. Else an excerpt. """
        if(self.meta_description):
            return(self.meta_description)
        return(strip_tags(mark_safe(self.body))[:150] +"...")

    def get_comment_count(self):
        """ Returns amount of comments in this post """
        comments_count = Comment.objects.filter(post = self).count()
        return(comments_count)

    class Meta:
        ordering = ('-publish',)
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __str__(self):
        return self.title
    
    def get_discussion_url(self):
        return reverse('blog:post_discussion', args=[self.publish.year,
                                                 self.publish.strftime('%m'),
                                                 self.publish.strftime('%d'),
                                                 self.slug])

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.strftime('%m'),
                                                 self.publish.strftime('%d'),
                                                 self.slug])

# Delete cover image on deletion
@receiver(post_delete, sender = Post)
def delete_post_image(sender, instance, **kwargs):
    """ Deletes media objects on deletion of this model """
    instance.cover_image.delete(False)  

#----------------------------------------

class Flatpage(models.Model):
    """ Flat pages, not belonging to the blog """
    
    STATUS_CHOICES = (
        ('draft', _('Draft')),
        ('published', _('Published')),
    )
    
    author = models.ForeignKey(User, related_name = 'flat_pages', on_delete = models.CASCADE, verbose_name = _('Author'))
    title = models.CharField(max_length = 250, verbose_name = _('Title'))
    slug = models.SlugField(max_length = 250, unique_for_date = 'created')
    meta_title = models.CharField(max_length = 250, blank = True, null = True, 
                                  verbose_name = _('Meta title'), 
                                  help_text = _("Optional SEO meta-title for this flatpage"))
    meta_description = models.CharField(max_length = 250, blank = True, null = True, 
                                        verbose_name = _('Meta description'), 
                                        help_text = _("Optional SEO meta-description for this flatpage"))
    body = models.TextField(verbose_name = _('Body'), help_text = _("Content of this page in plain text/mark-down format, without H1 tags"))
    cover_image = models.ImageField(upload_to = 'flatpage/%Y/%m/%d/', blank = True, null = True, verbose_name = _('Cover Image'))
    gallery = models.ForeignKey(PhotoGallery, related_name = 'flat_pages', on_delete = models.CASCADE, blank = True, null = True,
                                verbose_name = _('Gallery'),
                                help_text = _("Create or link a photo gallery."))
    status = models.CharField(max_length = 10, choices = STATUS_CHOICES, default = 'draft', verbose_name = _('Status'))
    created = models.DateTimeField(auto_now_add = True, verbose_name = _('Created')) 
    updated = models.DateTimeField(auto_now = True, verbose_name = _('Updated'))

    # Our managers
    objects = models.Manager()     # The default manager.

    def get_meta_title(self):
        """ Returns the meta title if defined. Else the post title. """
        if(self.meta_title):
            return(self.meta_title)
        return(self.title)
    
    def get_meta_description(self):
        """ Returns the meta description if defined. """
        if(self.meta_description):
            return(self.meta_description)
        return(strip_tags(mark_safe(self.body))[:150] +"...")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:flatpage', args=[self.slug])
    
    class Meta:
        ordering = ('-status',)
        verbose_name = _('Flatpage')
        verbose_name_plural = _('Flatpages')

# Delete cover image on deletion
@receiver(post_delete, sender = Flatpage)
def delete_page_image(sender, instance, **kwargs):
    """ Deletes media objects on deletion of this model """
    instance.cover_image.delete(False)  

#----------------------------------------

class Comment(models.Model):
    """ Comments """

    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'comments', verbose_name = _('Post'))
    name = models.CharField(max_length = 80, verbose_name = _('Name'))
    email = models.EmailField()
    body = models.TextField(verbose_name = _('Body'))
    created = models.DateTimeField(auto_now_add = True, verbose_name = _('Created')) 
    updated = models.DateTimeField(auto_now = True, verbose_name = _('Updated'))
    active = models.BooleanField(default = False)

    def approve(self):
        """ Approves this comment to be shown in the website """
        self.active = True
        return self.save(update_fields = ['active'])
    
    def reject(self):
        """ Disproves this comment """
        self.active = False 
        return self.save(update_fields = ['active'])

    def trash(self):
        """ Deletes this comment """
        return self.delete()

    def gravatar_url(self):
        """ Gets the URL for the gravatar for this user """
        md5 = hashlib.md5(self.email.encode())
        digest = md5.hexdigest()
        return('http://www.gravatar.com/avatar/{}'.format(digest))
    
    def save(self, *args, **kwargs):
        """ Intercept comment and strip js, html and offensive code """
        self.body = strip_tags(self.body)
        return super(Comment, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ('created',)
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __str__(self):
        """ Returns the comment as humanized string """
        return('Comment by '+ format(self.name) +' on '+ format(self.post))