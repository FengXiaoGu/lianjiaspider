import requests, json, time
from bs4 import BeautifulSoup
import re, csv


def parse_one_page(url):
    headers = {
        'user-agent': 'Mozilla/5.0'
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    results = soup.find_all(class_="clear LOGCLICKDATA")

    for item in results:
        output = []
        # 从url中获得区域
        output.append(url.split('/')[-3])

        # 获得户型、面积、朝向等信息，有无电梯的信息可能会有缺失，数据清理可以很方便的处理
        info1 = item.find('div', 'houseInfo').text.replace(' ', '').split('|')
        for t in info1:
            output.append(t)

        # 获得总价
        output.append(item.find('div', 'totalPrice').text)

        # 获得年份信息，如果没有就为空值
        info2 = item.find('div', 'positionInfo').text.replace(' ', '')
        if info2.find('年') != -1:
            pos = info2.find('年')
            output.append(info2[pos - 4:pos])
        else:
            output.append(' ')

        # 获得单价
        output.append(item.find('div', 'unitPrice').text)
        # print(output)
        write_to_file(output)


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
    regions = ['yanta']
    for region in regions:
        for i in range(1, offset):
            if(i%10==0):
                print(region, i)
            # url = 'https://cq.lianjia.com/ershoufang/' + region + '/pg' + str(i) + '/'
            url = 'https://xa.lianjia.com/ershoufang/' + region + '/pg' + str(i) + '/'
            html = parse_one_page(url)
            # time.sleep(1)
            # print('{} has been writen.'.format(region))

main(10)