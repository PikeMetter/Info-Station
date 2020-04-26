#django
from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponse
#function
from info.views import CommonViewMixin
from .models import Link

from pymongo import MongoClient
from pyecharts.charts import Line,Map,WordCloud
from pyecharts import options as opts
import json
import time
import pymongo

# Create your views here.
class LinkListView(CommonViewMixin,ListView):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    template_name = 'config/links.html'
    context_object_name = 'link_list'


def get_data(type_):
    '''
    返回用于制作地理热力图的数据，省份名和省份确诊数
    '''
    databaseIp='Ip号'
    databasePort=27017
    # 连接mongodb
    client = MongoClient(databaseIp, databasePort)
    mongodbName = '你的数据库名字'
    db = client[mongodbName]
    if type_ == 'map':
        collection = db.dxy_map
    elif type_ == 'dxy_count':
        collection = db.dxy_count
    elif type_ == 'line':
        collection = db.baidu_line
    else :
        collection = db.dxy_count
    alls = collection.find()
    return alls
cure_data = get_data('line')[0]

def timestamp_2_date(timestamp):
    '''
    用来将时间戳转为日期时间形式
    '''
    time_array = time.localtime(timestamp)
    my_time = time.strftime("%Y-%m-%d %H:%M", time_array)
    return my_time

def json_response(data, code=200):
    '''
    用于返回json数据，主要是将图表信息作为json返回
    '''
    data = {
        "code": code,
        "msg": "success",
        "data": data,
    }
    json_str = json.dumps(data)
    response = HttpResponse(
        json_str,
        content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response

JsonResponse = json_response

def yiqing(request):
    '''
    返回首页数据
    '''
    alls = get_data('dxy_count').sort("crawl_time", -1).limit(1)
    if alls:
        alls = alls[0]
    alls['modifyTime'] /= 1000
    alls['modifyTime'] = timestamp_2_date(alls['modifyTime'])
    return render(request, "blog/yiqing.html", alls)

def heat_map(request):
    '''
    地理热力图，以json返回
    '''
    map_data = []
    alls = get_data('map')
    for item in alls:
        # 将各省份名和确诊数组合成新的列表，以符合pyecharts map的输入
        map_data.append([item['provinceShortName'], item['confirmedCount']])
    # max_ = max([i[1] for i in map_data])
    # max_ = max([i[1] for i in map_data])
    map1 = (
        Map()
        # is_map_symbol_show去掉默认显示的小红点
        .add("疫情", map_data, "china", is_map_symbol_show=False)
        .set_global_opts(
            #不显示legend
            legend_opts=opts.LegendOpts(is_show=False),
            title_opts=opts.TitleOpts(title="疫情地图"),
            visualmap_opts=opts.VisualMapOpts(
                # 最大值
                # max = max_,
                # 颜色分段显示
                is_piecewise=True,
                # 自定义数据段，不同段显示不同的自定义的颜色
                pieces=[
                 {"min": 1001,  "label": ">1000", 'color':'#70161d'},
                 {"max": 1000, "min": 500,  "label": "500-1000", 'color':'#cb2a2f'},
                 {"max": 499, "min": 100, "label": "100-499", 'color':'#e55a4e'},
                 {"max": 99, "min": 10, "label": "10-99", 'color':'#f59e83'},
                 {"max": 9, "min": 1, "label": "1-9",'color':'#fdebcf'},
             ]
                ),
        )
        # 获取全局 options，JSON 格式（JsCode 生成的函数带引号，在前后端分离传输数据时使用）
        .dump_options_with_quotes()
    )
    return JsonResponse(json.loads(map1))

def cure_line(request):
    '''
    治愈/死亡折线图，以json返回
    '''

    line2 = (
        Line()
        .add_xaxis(cure_data['updateDate'])
        .add_yaxis('治愈', cure_data['list'][2]['data'],color='#5d7092',linestyle_opts = opts.LineStyleOpts(width=2),is_smooth=True,label_opts=opts.LabelOpts(is_show=False))
        .add_yaxis('死亡', cure_data['list'][3]['data'],color='#29b7a3',is_smooth=True,linestyle_opts = opts.LineStyleOpts(width=2),label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
        title_opts=opts.TitleOpts(title='治愈/死亡累计趋势图',pos_top='top'),
        # x轴字体偏移45度
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            #is_smooth = True,
            # 显示分割线
            splitline_opts=opts.SplitLineOpts(is_show=True),
            # 不显示y轴的黑线
            axisline_opts=opts.AxisLineOpts(is_show=False),
        ),
        tooltip_opts=opts.TooltipOpts(
            # 启用提示线，当鼠标焦点在图上时会显现
            is_show=True, trigger="axis", axis_pointer_type="cross",
        ),
        )
        .dump_options_with_quotes()
    )
    return JsonResponse(json.loads(line2))

def confirm_line(request):
    '''
    确诊/疑似折线图，以json返回
    '''
    line2 = (
        Line()
        .add_xaxis(cure_data['updateDate'])
        .add_yaxis('确诊', cure_data['list'][0]['data'],color='#f9b97c',linestyle_opts = opts.LineStyleOpts(width=2),is_smooth=True,label_opts=opts.LabelOpts(is_show=False))
        .add_yaxis('疑似', cure_data['list'][1]['data'],color='#ae212c',linestyle_opts = opts.LineStyleOpts(width=2),is_smooth=True,label_opts=opts.LabelOpts(is_show=False))

        .set_global_opts(
        title_opts=opts.TitleOpts(title='确诊/疑似累计趋势图',pos_top='top'),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            splitline_opts=opts.SplitLineOpts(is_show=True),
            axisline_opts=opts.AxisLineOpts(is_show=False),
        ),
        tooltip_opts=opts.TooltipOpts(
            is_show=True, trigger="axis", axis_pointer_type="cross",
        ),
        )
        .dump_options_with_quotes()
    )
    return JsonResponse(json.loads(line2))

def word_cloud(request):
    with open('static/data/word_count.txt','r',encoding='utf-8') as f:
        li = eval(f.read())
    c = (
        WordCloud()
            .add("", li[:151], word_size_range=[20, 100], shape="circle")
            .set_global_opts(title_opts=opts.TitleOpts(title="舆论词云"))
            .dump_options_with_quotes()
    )
    return JsonResponse(json.loads(c))