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

# 将 24 小时制时间转换为分钟数表示，0 时按 24 时计算
def minutes(time):
 
    if "（到达）" in time:
        time = time.replace('（到达）',"")
    
    elif "(到达)" in time:
        time = time.replace('(到达)',"")
        
    if "­" in time:
        time = time.replace('­', '')
        
    if ":" in time:
        hour_minute = time.split(":")
        hour = int(hour_minute[0])
        if hour == 0:
            hour = 24
        minute = int(hour_minute[1])
        return str(60*hour + minute)
    elif "：" in time:
        hour_minute = time.split("：")
        hour = int(hour_minute[0])
        if hour == 0:
            hour = 24
        minute = int(hour_minute[1])
        return str(60*hour + minute)
    else:
        return '-1'
# 将 dict 类型数据写入 CSV 文件
def write_csv_row(path_to_file, fieldnames, row):
    with open(path_to_file, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(row)

def get_all_lines_time():
    with open(times_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=times_header)
        writer.writeheader()
    with open(stations_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=stations_header)
        writer.writeheader()
    i= 0
    for url in urls:
            get_one_line_time(url,i)      #获取所有线路的数据
            i= i+1
        
        
def get_one_line_time(url,i):
    html = get_html(url)     #获取html页面
    bsobj = BeautifulSoup(html,"lxml")      #用lxml解析html
    bsobj.table  # 可以直接获取table元素
    if i==3:
        tbody = bsobj.find("table",{"bgcolor":"#ffffff"}).find("tbody")
    elif i==5:
        tbody = bsobj.findAll("table")[0].find("tbody")
    else:
        tbody = bsobj.find("table",{"bgcolor":"#999999"}).find("tbody")

    while tbody is None:
        print("        retry ...")
        html = get_html(url)
        bsobj = BeautifulSoup(html, "lxml")
        tbody = bsobj.find("table",{"bgcolor":"#999999"}).find("tbody")
    
    trs = tbody.findAll("tr")           #把所有行放入数组trs[]
    stations = []
    lines = [3, 5, 6, 12, 13, 16]
    global number
    global station_names

    #####3、5、6、12、13、16号线#######

    for tr in trs[2:]:                 #跳过前两行的标题内容，开始遍历列行
        tds = tr.findAll("td")         #把一行中的所有列放入数组tds[]
        line = lines[i]                #地铁线路

        ###########处理方向1#############
        station_name = tds[0].get_text()
        toStart_first_time = minutes(tds[1].get_text())  #方向1首班车出发时间
        toEnd_last_time = minutes(tds[3].get_text())   #方向1晚班车出发时间
        toStart_first_time2 = minutes(tds[2].get_text())   #方向2首班车出发时间
        toEnd_last_time2 = minutes(tds[4].get_text())    #方向2晚班车出发时间
        station = [line, station_name, toStart_first_time, toEnd_last_time, toStart_first_time2, toEnd_last_time2]
        stations.append(station)
        
        ############ 爬取所有站点的名称，并给每个站点编一个唯一的编号##
        if station_name in station_names:
             continue
        else:
            station_names[station_name] = number
            row ={'station_name':station_name, 'number':number}
            write_csv_row(stations_file, stations_header, row)
            number += 1
                 
    n = len(stations)
    ###########写方向1和方向2#############
    for i in range(n-1):
        row = { "line": line, "from_station": stations[i+1][1], "to_station": stations[i][1], "first_time": stations[i+1][2], "last_time": stations[i+1][3],}
        write_csv_row(times_file, times_header, row)
    for i in range(n-1):    
        row = { "line": line, "from_station": stations[i][1], "to_station": stations[i+1][1], "first_time": stations[i][4], "last_time": stations[i][5],}
        write_csv_row(times_file, times_header, row)
        
######3、5、6、12、13、16号线
lines = ["245.htm", "247.htm", "248.htm","254.htm", "255.htm","256.htm"]
station_names = {}  
number = 1
urls = ["http://service.shmetro.com/hcskb/%s" % line for line in lines]
stations_file = 'stations.csv'
times_file = 'time2.csv'
times_header = ['line', 'from_station', 'to_station', 'first_time', 'last_time']
times_weekend_file = 'time_weekend.csv'
stations_header = ['station_name', 'number']
get_all_lines_time()

