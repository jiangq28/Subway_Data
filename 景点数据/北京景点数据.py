import urllib.request
import json
import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
# 获取页面源码
def get_html(url):
    browser = webdriver.PhantomJS(executable_path=r"E:/spider/phantomjs-2.1.1-windows/bin/phantomjs.exe")     #使用无界面的phantomjs浏览器
    browser.get(url)                 #发送请求
    print("### Handling <" + url + ">")
    return browser.page_source


def get_info(url, city, file):
    with open(file, 'w') as csvfile:
        writer = csv.writer(csvfile)
    html = get_html(url)     #获取html页面
    bsobj = BeautifulSoup(html, "lxml")       #用lxml解析html
    tbody = bsobj.find("tbody")    #查找到显示线路信息的表格
   
    while tbody is None:
        print("        retry ...")
        html = get_html(url)
        bsobj = BeautifulSoup(html, "lxml")
        tbody = bsobj.find("tbody")
        
    trs = tbody.findAll("tr")           #把所有行放入数组trs[]
    infos = []
    for tr in trs:                 #开始遍历列车行
        tds = tr.findAll("td")         #把一行中的所有列放入数组tds[]
        number = tds[0].get_text()  #序号
        name = tds[1].get_text()    #名称
        level = tds[2].get_text()   #等级
        address = tds[4].get_text().split()[0]    #地址
        
        info = [number, name, level, address,]
        print(info)
        with open(file, 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(info)
    print("        [success]")


out_file = '北京市景点.csv'
urls = ['http://www.bjta.gov.cn/tsfwzt/qyml/394778.htm']

###########30个城市的名字##########
city = ['BeiJing','ShangHai','GuangZhou','ShenZhen','WuHan','TianJin','NanJing',
        'XiangGang','ChongQin','HangZhou','ShenYang','DaLian','ChengDu','ChangChun',
        'SuZhou','FoShan','KunMing','XiAn','ZhengZhou','ChangSha','NingBo',
        'WuXi','QingDao','NanChang','FuZhou','DongGuan','NanNing','HeFei',
        'HaErbin','ShiJiazhuang'
        ]
for i in range(len(urls)):
    get_info(urls[i],city[i],out_file)
