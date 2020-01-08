from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Category, Post, Comment, Tag, PhotoGallery, Profile, Flatpage
from django.forms import TextInput, Textarea
from django.db import models

class ProfileInline(admin.StackedInline):
    """ Stacked inline profile extending the user model to store additional user information """
    model = Profile
    can_delete = False
    verbose_name_plural = 'Blog User Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        """ Return inline instances for admin, or super ones """
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

# De-register user model
admin.site.unregister(User)

# Register ours instead, with our admin settings
admin.site.register(User, CustomUserAdmin)

class PhotoGalleryAdmin(admin.ModelAdmin):
    """ Admin config class for the Photo Gallery model """
    list_display = ('title',)
    search_fields = ('title',)
    date_hierarchy = 'created'
    ordering = ['created', 'updated']
    list_filter  = ('created',)
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80%'})},
    }
admin.site.register(PhotoGallery, PhotoGalleryAdmin)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'created'
    ordering = ['created', 'updated']
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80%'})},
    }
admin.site.register(Tag, TagAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug','description')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'created'
    ordering = ['created', 'updated']
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80%'})},
    }
admin.site.register(Category, CategoryAdmin)

class PostAdmin(admin.ModelAdmin):
    """ Admin config class for the Post model """
    list_display = ('title', 'category','author','status')
    list_filter = ('status', 'created', 'publish', 'author','category')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author','gallery')
    date_hierarchy = 'publish'
    ordering = ['status', '-publish']
    filter_horizontal = ('tags',)
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80%'})},
    }
admin.site.register(Post, PostAdmin)

class FlatpageAdmin(admin.ModelAdmin):
    """ Admin config class for flat pages """
    list_display = ('title','author','status')
    list_filter = ('status','created','author')
    search_fields = ('title','body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'created'
    ordering = ['status', '-created']
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80%'})},
    }
admin.site.register(Flatpage, FlatpageAdmin)

class CommentAdmin(admin.ModelAdmin):
    """ Admin config class for the Comment model """
    list_display = ('email','body','created','active')
    list_filter  = ('active','created','updated')
    search_fields = ('name', 'email','body')
    ordering = ['active','created']
    
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80%'})},
    }

    # Admin Actions
    actions = ['make_approved','make_rejected']

    # Admin actions definitions
    def make_approved(self, request, queryset):
        """ Approve selected comments """

        rows_updated = queryset.update(active = True)
        if rows_updated == 1:
            message_bit = "1 comment"
        else:
            message_bit = str(rows_updated) +" comments were "
        self.message_user(request, "%s successfully approved." % message_bit)
    make_approved.short_description = "Approve selected comments"
    
    def make_rejected(self, request, queryset):
        """ Reject selected comments """

        rows_updated = queryset.update(active = False)
        if rows_updated == 1:
            message_bit = "1 comment"
        else:
            message_bit = str(rows_updated) +" comments were "
        self.message_user(request, "%s successfully rejected." % message_bit)
    make_rejected.short_description = "Reject selected comments"
    
admin.site.register(Comment, CommentAdmin)