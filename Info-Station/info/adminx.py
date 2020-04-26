#django
from django.contrib import admin
from django.utils.html import format_html
#from models
from .models import Post, Category, Tag
#InfoStation
from InfoStation.base_admin import BaseOwnerAdmin
from InfoStation import custom_site
#xadmin
import xadmin
from xadmin.filters import RelatedFieldListFilter
from xadmin.filters import manager
from xadmin.layout import Row,Fieldset,Container
from .adminforms import PostAdminForm

# Register your models here.
@xadmin.sites.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    # inlines = [PostInline,]
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')  # 页面提交之后展示的字段
    fields = ('name', 'status', 'is_nav')  # 控制页面要展示的字段

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'

class CategoryOwnerFilter(RelatedFieldListFilter):
    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        # 重新获取lookup_cookies,根据owner过滤
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')

manager.register(CategoryOwnerFilter, take_priority=True)

@xadmin.sites.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

@xadmin.sites.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = [
        'title', 'category', 'status',
        'created_time','operator', 'owner',
    ]
    list_display_links = []
    list_filter = ['category']
    search_fields = ['title', 'category__name']
    save_on_top = True
    actions_on_top = True
    actiosn_on_bottom = True
    exclude = ['owner', ]
    # 编辑页面
    save_on_top = True
    form_layout = (
        Fieldset(
            '基础信息',
            Row("title", "category"),
            'status',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'content',
            'is_md',
            'content_ck',
            'content_md',
        )
    )
    def operator(self,obj):
        return format_html(
            '<a href="{}">编辑</a>',
            self.model_admin_url('change',obj.id)
            # reverse('xadmin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'

    class Meida:
        css = {
            'all':('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css',),
        }
        js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)