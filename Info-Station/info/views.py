#django
from django.shortcuts import render
from django.views.generic import DetailView,ListView
from django.shortcuts import get_object_or_404
from django.db.models import Q,F
from django.core.cache import cache
from django.views.generic import TemplateView
#function
from datetime import date
from .models import Post,Tag,Category
from config.models import SideBar
# Create your views here.

class IndexView(TemplateView):
    def get(self, request):
        return render(request, 'blog/shouye.html', {"name": "index", })

class CommonViewMixin:
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars':SideBar.get_all(),
        })
        context.update(Category.get_navs())
        return context

class ArticleView(CommonViewMixin,ListView):
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL) \
        .select_related('owner') \
        .select_related('category')
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/list.html'

class CategoryView(ArticleView):
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category,pk=category_id)
        context.update({
            'category':category,
        })
        return context
    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)

class TagView(ArticleView):
    # 获得tag并且对404作出处理
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag,pk=tag_id)
        context.update({
            'tag':tag,
        })
        return context
    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)

class PostDetailView(CommonViewMixin,DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get(self,request,*args,**kwargs):
        response = super().get(request,*args,**kwargs)
        self.handle_visited()
        return response

    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        pv_key = 'pv:%s:%s'%(uid,self.request.path)
        uv_key = 'uv:%s:%s:%s'%(uid,str(date.today()),self.request.path)
        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key,1,1*60)#1分钟有效
        if not cache.get(uv_key):
            increase_uv = True
            cache.set(pv_key,1,24*60*60)#24小时有效
        if increase_pv and increase_uv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv')+1,uv=F('uv')+1)
        elif increase_pv :
            Post.objects.filter(pk=self.object.id).update(pv=F('pv')+1)
        elif increase_uv:
            Post.objects.filter(pk=self.object.id).update(uv=F('uv')+1)

class SearchView(ArticleView):
    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'keyword':self.request.GET.get('keyword','')
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword)|Q(desc__icontains=keyword))

class AuthorView(ArticleView):
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id = author_id)


def about(request):
    return render(request, 'blog/about.html',{'name':'about'})