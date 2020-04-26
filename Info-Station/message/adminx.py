from django.contrib import admin
import xadmin
from .models import Message
# Register your models here.

@xadmin.sites.register(Message)
class CommentAdmin:
    # 模型字段的后台显示
    list_display = ['name', 'website','email', 'message', 'created_time']
    # 字段的后台搜索功能（搜索依据的字段），时间不要做为搜索的条件，显示会有问题
    search_fields = ['name', 'website', 'email','message']
    # 字段的筛选功能，用于数据的显示
    list_filter = ['name','website', 'email',  'message', 'created_time']