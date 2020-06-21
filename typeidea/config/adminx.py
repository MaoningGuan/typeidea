import xadmin

from django.contrib import admin

from .models import Link, SideBar
from typeidea.base_admin import BaseOwnerAdmin


# Register your models here.
@xadmin.sites.register(Link)
class LinkAdmin(BaseOwnerAdmin):
    list_display = ('title', 'href', 'status', 'weight', 'owner', 'created_time')
    fields = ('title', 'href', 'status', 'weight')


@xadmin.sites.register(SideBar)
class SideBarAdmin(BaseOwnerAdmin):
    list_display = ('title', 'display_type', 'content', 'owner', 'created_time')
    fields = ('title', 'display_type', 'content')
