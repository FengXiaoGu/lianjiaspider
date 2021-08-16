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
    f = open('二手房信息.csv', mode='a', encoding='utf-8-sig', newline='')
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


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }
    url = 'https://xa.lianjia.com/ershoufang/101112358501.html'

    response = requests.get(url=url, headers=headers)
    selector = parsel.Selector(response.text)
    lis1 = selector.css('.base li')
    lis1[1].css("li::text").get()
    lis2 = selector.css('.transaction li')
    lis2[1].css("span::text").getall()
    box1 = selector.css('.box-1 li')
    title = selector.css('.title a::text').get()

    lis3 = selector.css(r"descendant-or-self::*[@class and contains(concat(' ', normalize-space(@class), ' '), ' base ')]/descendant-or-self::*/li")


    for li in lis1:
        title = li.css('a::text').get()
        print(title)


main(101)