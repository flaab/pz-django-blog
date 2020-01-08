from django.conf.urls import include, url
from django.urls import path, include
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap 
from blog.sitemaps import PostSiteMap, CategorySiteMap, TagSiteMap
from django.conf.urls.static import static
from . import settings 

sitemaps = {
    'posts': PostSiteMap,
    'categories': CategorySiteMap,
    'tags': TagSiteMap,
}

urlpatterns = [
    path('', include(('blog.urls', 'blogdefault'), namespace = 'blogdefault')),
    path('blog/', include(('blog.urls', 'blog'), namespace = 'blog')),
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name = 'django.contrib.settings.views.sitemap'),
]

if(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)