from django.contrib.admin import AdminSite

class CustomSite(AdminSite):
    site_header = '信息站'
    site_title = '信息站'
    index_title = '首页'

custom_site = CustomSite(name = 'cus_admin')