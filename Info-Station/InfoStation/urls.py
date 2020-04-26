"""InfoStation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#django
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
# 静态文件服务器模块
from django.views.static import serve
from InfoStation import settings
from django.conf.urls.static import static
#function
from config.views import LinkListView
from info.views import (
    IndexView,CategoryView,TagView,PostDetailView,SearchView,AuthorView,about,ArticleView
)
from message.views import MessageView,AddMessageView
import config.views as confviews
#xadmin
import xadmin


urlpatterns = [
    path('xadmin/',  xadmin.site.urls, name='xadmin'),
    path('links/', LinkListView.as_view(), name='links'),
    path('category/<int:category_id>/', CategoryView.as_view(), name='category-list'),
    path('',IndexView.as_view(),name='index'),
    path('article/', ArticleView.as_view(), name='article'),
    path('tag/<int:tag_id>/', TagView.as_view(), name='tag-list'),
    path('post/<int:post_id>.html', PostDetailView.as_view(), name='post-detail'),
    path('search/', SearchView.as_view(), name='search'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('author/<int:owner_id>/', AuthorView.as_view(), name='author'),
    path('about/', about, name='about'),
    path('message/',MessageView.as_view(),name = 'message'),
    path('add-message/', AddMessageView.as_view(), name="add-message"),

    path('yiqing/', confviews.yiqing, name='yiqing'),
    path('demo/word_cloud/', confviews.word_cloud, name='word_cloud'),
    path('demo/map/', confviews.heat_map, name='map'),
    path('demo/cure_line/', confviews.cure_line, name='cure_line'),
    path('demo/confirm_line/', confviews.confirm_line, name='confirm_line'),
    # 配置图片请求
   #  path('media/<path:path>/', serve, {'document_root': settings.MEDIA_ROOT}),
   # 配置静态文件路径，用于调试 404 等错误页面
   #  path('static/<path:path>/', serve, {'document_root': settings.STATIC_ROOT}),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

# 404 错误页面 （一般是错误的 url 导致的)
handler400 = "message.views.handler_400_error"
handler403 = "message.views.handler_403_error"
handler404 = "message.views.handler_404_error"
handler500 = "message.views.handler_500_error"