# 二手房 爬虫

# 2021/08/16

# FengXiaoGu



# 加入了代理
# 加入了多线程
import requests, json, time
from bs4 import BeautifulSoup
import re, csv
import requests
import parsel
import time
import multiprocessing

import csv


PROXY_POOL_URL = 'http://localhost:5555/random'

def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None




def process(id0):


    hds = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
           {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
           {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
           {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},
           {'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
           {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
           {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},
           {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
           {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},
           {'User-Agent': 'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},
           {'User-Agent': 'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}]

    with open('result/right/'+str(id0)+'二手房详情.csv', mode='a', encoding='utf-8-sig', newline='') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=['链家编号', '小区名称', '所在区域', '总价', '单价', '房屋户型', '所在楼层', '建筑面积',
                                                   '户型结构', '套内面积', '建筑类型', '房屋朝向', '建筑结构', '装修情况', '梯户比例',
                                                   '供暖方式', '配备电梯', '挂牌时间', '交易权属', '上次交易', '房屋用途', '房屋年限',
                                                   '产权所属', '抵押信息', '房本备件', '小区均价', '建筑年代', '建筑楼型', '楼栋总数'])
        csv_writer.writeheader()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }
    id0 = id0
    for i in range(100000):
        proxie_ip = {'http': get_proxy()}

        dit = {}
        id = id0+i

        if (i % 1000 == 0):
            print(id)
        url = 'https://xa.lianjia.com/ershoufang/' + str(id) + '.html'
        # url = 'https://xa.lianjia.com/ershoufang/101112602555.html'
        response = requests.get(url=url, headers=hds[i%12], proxies= proxie_ip)
        selector = parsel.Selector(response.text)

        lis_base = selector.css('.base li')
        if 0 == len(lis_base):
            continue

        try:
            dit['单价'] = float(selector.css('.unitPrice span::text').get())
            dit['总价'] = float(selector.css('.price span::text').get())
            dit['链家编号'] = id
            dit['小区名称'] = selector.css('.communityName a::text').get()
            dit['所在区域'] = '-'.join(selector.css('.areaName a::text').getall())

            lis_base = selector.css('.base li')
            if 0 == len(lis_base):
                continue

            for li in lis_base:
                att = li.css('::text').getall()
                dit[att[0].replace('\n', '').replace(' ', '')] = att[1].replace('\n', '').replace(' ', '')

            lis_transaction = selector.css('.transaction li')
            for li in lis_transaction:
                att = li.css("span::text").getall()
                dit[att[0].replace('\n', '').replace(' ', '')] = att[1].replace('\n', '').replace(' ', '')

            # lis_xiaoqu = selector.css('*xiaoqu*')

            with open('result/right/'+str(id0)+'二手房详情.csv', mode='a', encoding='utf-8-sig', newline='') as csvfile:
                csv_writer = csv.DictWriter(csvfile, fieldnames=['链家编号', '小区名称', '所在区域', '总价', '单价', '房屋户型', '所在楼层', '建筑面积',
                                                           '户型结构', '套内面积', '建筑类型', '房屋朝向', '建筑结构', '装修情况', '梯户比例',
                                                           '供暖方式', '配备电梯', '挂牌时间', '交易权属', '上次交易', '房屋用途', '房屋年限',
                                                           '产权所属', '抵押信息', '房本备件', '小区均价', '建筑年代', '建筑楼型', '楼栋总数'])
                # writer = csv.writer(csvfile)
                csv_writer.writerow(dit)

        except:

            with open('result/wrong/'+str(id0)+"wrong.txt", "a") as f:
                f.write(str(id)+ '  wrong\n')
            print(id, 'wrong')






if __name__ == '__main__':
    id0 = 101110000000
    for i in range(100):
        id = id0 + i*100000
        p = multiprocessing.Process(target=process, args=(id,))
        p.start()