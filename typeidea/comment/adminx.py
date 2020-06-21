import xadmin

from django.contrib import admin

from .models import Comment


# Register your models here.
@xadmin.sites.register(Comment)
class CommentAdmin(object):
    list_display = ('target', 'target_title', 'nickname', 'content', 'website', 'created_time')
