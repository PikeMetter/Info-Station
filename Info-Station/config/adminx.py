from django.contrib import admin
from .models import Link,SideBar

from InfoStation.custom_site import custom_site
from InfoStation.base_admin import  BaseOwnerAdmin
import xadmin
# Register your models here.
@xadmin.sites.register(Link,site = custom_site)
class LinkAdmin(BaseOwnerAdmin):
    list_display = ('title', 'href', 'status', 'weight', 'created_time')
    fields = ('title', 'href', 'status', 'weight')

@xadmin.sites.register(SideBar,site = custom_site)
class SideBarAdmin(BaseOwnerAdmin):
    list_display = ('title', 'display_type', 'content', 'created_time')
    fields = ('title', 'display_type', 'content')