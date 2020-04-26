import requests
import json
import re
import time
from time import sleep
from pymongo import MongoClient
import schedule
import pymongo


def insert_item(item, type_):
    '''
    插入数据到mongodb，item为要插入的数据，type_用来选择collection
    '''
    databaseIp='你的IP'
    databasePort=27017
    client = MongoClient(databaseIp, databasePort)
    mongodbName = '你数据库的名字'
    db = client[mongodbName]
    if type_ == 'dxy_map':
        # 更新插入
        db.dxy_map.update({'id': item['provinceName']}, {'$set': item}, upsert=True)
    elif type_ == 'dxy_count':
        # 直接插入
        db.dxy_count.insert_one(item)
    else:
        # 更新插入
        db.baidu_line.update({},{'$set': item}, upsert=True)
    print(item,'插入成功')
    client.close()

def dxy_spider():
    '''
    丁香园爬取，获取各省份的确诊数，用来做地理热力图
    '''
    time_result = {}
    all_result = {}
    url = 'https://ncov.dxy.cn/ncovh5/view/pneumonia'
    r = requests.get(url)
    r.encoding = 'utf-8'
    #res = re.findall('tryTypeService1 =(.*?)}catch', r.text, re.S)
    res = re.findall('getListByCountryTypeService2true =(.*?)}catch', r.text, re.S)
    if res:
        # 获取数据的修改时间
        time_result = json.loads(res[0])
    res = re.findall('getAreaStat =(.*?)}catch', r.text, re.S)
    if res:
        # 获取省份确诊人数数据
        all_result = json.loads(res[0])
    #for times in time_result:
    for item in all_result:
        #if times['provinceName'] == item['provinceName']:
            # 因为省份确诊人数的部分没有时间，这里将时间整合进去
            #item['createTime'] = times['createTime']
            #item['modifyTime'] = times['modifyTime']
            insert_item(item, 'dxy_map')

    count = re.findall('getStatisticsService =(.*?)}catch', r.text, re.S)
    if count:
        count_res = json.loads(count[0])
        count_res['crawl_time'] = int(time.time())
        # if count_res.get('confirmedIncr') > 0:
        #     count_res['confirmedIncr'] = '+' + str(count_res['confirmedIncr'])
        # if count_res.get('seriousIncr') > 0:
        #     count_res['seriousIncr'] = '+' + str(count_res['seriousIncr'])
        # if count_res.get('curedIncr') > 0:
        #     count_res['curedIncr'] = '+' + str(count_res['curedIncr'])
        # if count_res.get('deadIncr') > 0:
        #     count_res['deadIncr'] = '+' + str(count_res['deadIncr'])
        insert_item(count_res, 'dxy_count')

def baidu_spider():
    '''
    百度爬虫，爬取历史数据，用来画折线图
    '''
    url = 'https://voice.baidu.com/act/newpneumonia/newpneumonia'
    r = requests.get(url=url)
    res = re.findall('"degree":"3408"}],"trend":(.*?]}]})',r.text,re.S)
    data = json.loads(res[0])
    insert_item(data,'baidu_line')# def main():

def main():
     dxy_spider()
     baidu_spider()


if __name__ == '__main__':
    # dxy_spider()
    # baidu_spider()
    schedule.every().day.at("12:00").do(main)
    while True:
        schedule.run_pending()
        sleep(10)