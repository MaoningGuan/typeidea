"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import xadmin
from .autocomplete import CategoryAutocomplete, TagAutocomplete

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps import views as sitemap_views

from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap
from blog.views import (
    IndexView, CategoryView, TagView,
    PostDetailView, SearchView, AuthorView
)
from comment.views import CommentView
from config.views import LinkListView
from .custom_site import custom_site

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),  # 首页
    url(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category-list'),  # 分类列表页
    url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag-list'),  # tag列表页
    url(r'post/(?P<post_id>\d+).html$', PostDetailView.as_view(), name='post-detail'),  # 文章详情页
    url(r'^links/$', LinkListView.as_view(), name='links'),  # 友链页
    url(r'^search/$', SearchView.as_view(), name='search'),  # 搜索页
    url(r'^author/(?P<owner_id>\d+)/$', AuthorView.as_view(), name='author'),  # 作者页面
    url(r'^comment/$', CommentView.as_view(), name='comment'),  # 评论提交
    url(r'^rss|feed/', LatestPostFeed(), name='rss'),  # RSS订阅
    url(r'^sitemap\.xml$', sitemap_views.sitemap, {'sitemaps': {'posts': PostSitemap}}),  # sitemap，用于搜索引擎的收录
    url(r'^category-autocomplete/$', CategoryAutocomplete.as_view(),
        name='category-autocomplete'),  # 分类自动补全
    url(r'^tag-autocomplete/$', TagAutocomplete.as_view(),
        name='tag-autocomplete'),  # 标签自动补全
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),  # 富文本编辑器上传图片接口

    url(r'^admin/', xadmin.site.urls, name='xadmin'),  # 后套管理
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
