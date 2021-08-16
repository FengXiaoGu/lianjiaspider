import requests
import parsel
import time

import csv

f = open('二手房信息.csv', mode='a', encoding='utf-8-sig', newline='')
csv_writer = csv.DictWriter(f, fieldnames=['标题', '开发商', '房子信息', '发布周期', '售价/万', '单价'])
csv_writer.writeheader()

for page in range(1, 101):
    print('===========================正在下载第{}页数据================================'.format(page))
    time.sleep(1)
    url = 'https://xa.lianjia.com/ershoufang/pg{}/'.format(page)
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
        print(dit)

