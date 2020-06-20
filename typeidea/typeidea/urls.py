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
from django.conf.urls import url
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

    url(r'^super_admin/', admin.site.urls, name='super-admin'),
    # url(r'^admin/', admin.site.urls),
    url(r'^admin/', custom_site.urls, name='admin')
]
