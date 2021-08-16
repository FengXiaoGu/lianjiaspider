# 二手房 爬虫

# 2021/08/16

# FengXiaoGu



import requests, json, time
from bs4 import BeautifulSoup
import re, csv
import requests
import parsel
import time


import csv

def parse_one_page(url):
    f = open('西安二手房信息.csv', mode='a', encoding='utf-8-sig', newline='')
    csv_writer = csv.DictWriter(f, fieldnames=['标题', '开发商', '房子信息', '发布周期', '售价/万', '单价'])
    csv_writer.writeheader()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }

    response = requests.get(url=url, headers=headers)
    selector = parsel.Selector(response.text)
    lis = selector.css('.sellListContent li')
    dit = {}
    for li in lis:
        title = li.css('.title a::text').get()
        dit['标题'] = title
        positionInfo = li.css('.positionInfo a::text').getall()
        info = '-'.join(positionInfo)
        dit['开发商'] = info
        houseInfo = li.css('.houseInfo::text').get()
        dit['房子信息'] = houseInfo
        followInfo = li.css('.followInfo::text').get()
        dit['发布周期'] = followInfo
        Price = li.css('.totalPrice span::text').get()
        dit['售价/万'] = Price
        unitPrice = li.css('.unitPrice span::text').get()
        dit['单价'] = unitPrice
        csv_writer.writerow(dit)
        # print(dit)


def write_to_file(content):
    # 参数newline保证输出到csv后没有空行
    with open('data.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # writer.writerow(['Region', 'Garden', 'Layout', 'Area', 'Direction', 'Renovation', 'Elevator', 'Price', 'Year', 'PerPrice'])
        writer.writerow(content)


def main(offset):
    # regions = ['jiangbei', 'yubei', 'nanan', 'banan', 'shapingba', 'jiulongpo', 'yuzhong', 'dadukou', 'jiangjing',
    #            'fuling',
    #            'wanzhou', 'hechuang', 'bishan', 'changshou1', 'tongliang', 'beibei']

    regions = ['yanta', 'beilin', 'weiyang', 'baqiao', 'xinchengqu', 'lintong', 'yanliang', 'changan', 'lianhu']
    # regions = ['yanta']
    for region in regions:
        for i in range(1, offset):
            # url = 'https://cq.lianjia.com/ershoufang/' + region + '/pg' + str(i) + '/'
            url = 'https://xa.lianjia.com/ershoufang/' + region + '/pg' + str(i) + '/'
            html = parse_one_page(url)
            if(i%10==0):
                print(region, i)
            # time.sleep(1)
            # print('{} has been writen.'.format(region))

main(101)