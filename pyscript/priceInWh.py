
# Vegetable prices in wuhan

import requests
from bs4 import BeautifulSoup
import re
import math
import pymysql.cursors
import time

proxies = {
    "http": "10.25.192.8:8080",
    "https": "10.25.192.8:8080"
}
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
}
session = requests.Session()

baseUrl = 'http://www.whbsz.com.cn/Price.aspx?Type=1'
pageSuffix = '&PageNo='

all_price_info = []
today = time.strftime('%Y-%m-%d', time.localtime(time.time()))

try:
    result = session.get(baseUrl, proxies=proxies, headers=header)
    soup = BeautifulSoup(result.text, 'html.parser')
except Exception:
    print(Exception.message)

# 查询目前有多少条蔬菜价格信息，看看是否需要翻页
pageInfoSpan = soup.find("span", {"id": "cphRight_lblRecord", "class": "Small"})
pageInfo = pageInfoSpan.get_text()
pageinfos = re.compile(r'\d+').findall(pageInfo)
if pageinfos and len(pageinfos) == 3:
    pageCount = math.ceil(int(pageinfos[0]) / int(pageinfos[2]))
    print('共有菜价数据 %s 条,每页显示 %s 条, 共有 %d 页' % (pageinfos[0], pageinfos[2], pageCount))

# 处理第一页的蔬菜价格
alltr = soup.find_all("tr", {"onclick": re.compile("opdlg\w*")})
for tr in alltr:
    allTd = tr.find_all("td")
    one_price_info = []
    if allTd and len(allTd) == 6:
        one_price_info.append("".join(allTd[0].get_text().split()))
        one_price_info.append("".join(allTd[2].get_text().split()))
        one_price_info.append("".join(allTd[3].get_text().split()))
        one_price_info.append("".join(allTd[4].get_text().split()))
    all_price_info.append(one_price_info)
# 处理其他页的蔬菜价格
for num in range(2, pageCount + 1):
    try:
        newUrl = baseUrl + pageSuffix + str(num)
        result = session.get(newUrl, proxies=proxies, headers=header)
        soup = BeautifulSoup(result.text, 'html.parser')
    except Exception:
        print(Exception.message)

    alltr = soup.find_all("tr", {"onclick": re.compile("opdlg\w*")})
    for tr in alltr:
        allTd = tr.find_all("td")
        one_price_info = []
        if allTd and len(allTd) == 6:
            one_price_info.append("".join(allTd[0].get_text().split()))
            one_price_info.append("".join(allTd[2].get_text().split()))
            one_price_info.append("".join(allTd[3].get_text().split()))
            one_price_info.append("".join(allTd[4].get_text().split()))
        all_price_info.append(one_price_info)

# 将蔬菜价格逐条保存到数据库中
# 连接数据库
try:
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='root',
        db='pyspider',
        charset='utf8'
    )

    # 获取游标
    cursor = connect.cursor()
    sql = "INSERT INTO `pyspider`.`tb_wh_vegetables_price`(`name`, `price_max`, `price_min`, `price_avg`, `date_value`) VALUES ('%s','%.2f','%.2f','%.2f','%s')"

    for price_info in all_price_info:
        data = (price_info[0], float(price_info[1]), float(price_info[2]), float(price_info[3]), today)
        print(sql % data)
        cursor.execute(sql % data)
        connect.commit()
finally:
    # 关闭连接
    cursor.close()
    connect.close()
