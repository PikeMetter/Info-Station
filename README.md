

# 疫情之下，生命不息

#### 1.技术栈

```
前端：Bootstrap 搭建

后端：python3.6.2 + django2.0.9+xadmin2（需要单独安装）

部署：uWSGI+nginx
```

点击体验：[疫情之下，生命不息](https://hoha.site)

#### 2.主要功能

- 自动定时获取疫情信息，存储在mongodb
- pyecharts分析疫情
- 后台发布修改文章，支持md格式
- 留言功能

#### 3.修改settings文件

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'InfoStation',
        'USER': '',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'CONN_MAX_AGE': 5*60,
        'OPTIONS': {'charset': 'utf8mb4'}
    }
}
```

#### 4.修改config/views.py以及InfoStation/spider/spider.py

```
    databaseIp='127.0.0.1'
    databasePort=27017
    # 连接mongodb
    client = MongoClient(databaseIp, databasePort)
    mongodbName = '你的数据库名字'
```

#### 5.安装部署

```
安装依赖包
pip install -r requirments.txt

生成迁移文件
python manage.py makemigrations 

执行迁移文件
python manage.py migrate

启动项目
python manager.py runserver 

创建管理员账号
python manage.py createsuperuser
```

------

此Django项目已不再维护





