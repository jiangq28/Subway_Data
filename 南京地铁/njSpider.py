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
    if ":" in time:
        hour_minute = time.split(":")
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
    print("        [success]")
# 爬取所有站点的名称，并给每个站点编一个唯一的编号

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
    line_name = [1,2,3,4,10,"s1","s8","s3"]
    html = get_html(url)     #获取html页面
    bsobj = BeautifulSoup(html, "lxml")       #用lxml解析html
    tbody = bsobj.find("tbody")    #查找到显示线路信息的表格
    while tbody is None:
        print("        retry ...")
        html = get_html(url)
        bsobj = BeautifulSoup(html, "lxml")
        tbody = bsobj.find("tbody")    #查找到显示线路信息的表格
    trs = tbody.findAll("tr")           #把所有行放入数组trs[]
    stations = []
    global number
    global station_names
    
    for tr in trs:                 #跳过前三行的标题内容，开始遍历列车行
        tds = tr.findAll("td")         #把一行中的所有列放入数组tds[]
        line = line_name[i]
        station_name = tds[0].get_text()
        toStart_time = minutes(tds[1].get_text())  #方向1首班车时间
        toEnd_time = minutes(tds[3].get_text())    #方向1末班车时间
        toStart_time2 = minutes(tds[2].get_text())   #方向2首班车时间
        toEnd_time2 = minutes(tds[4].get_text())     #方向2末班车时间
        station = [line, station_name, toStart_time, toEnd_time, toStart_time2, toEnd_time2,]
        stations.append(station)

         # 爬取所有站点的名称，并给每个站点编一个唯一的编号
        if station_name in station_names:
            continue
        else:
            station_names[station_name] = number
            row ={'station_name':station_name, 'number':number}
            write_csv_row(stations_file, stations_header, row)
            number += 1
    n = len(stations)
    for i in range(n-1):       #方向1
        row = { "line": line, "from_station": stations[i][1], "to_station": stations[i+1][1], "first_time": stations[i][2], "last_time": stations[i][3],}
        write_csv_row(times_file, times_header, row)
    for i in range(n-1):     #方向2
        row = { "line": line, "from_station": stations[i+1][1], "to_station": stations[i][1], "first_time": stations[i+1][4], "last_time": stations[i+1][5],}
        write_csv_row(times_file, times_header, row)
number = 1
station_names = {}      
lines = ["x_44fac405", "x_0bd59b0e", "x_b4a482e2", "x_3717a1ad", "x_40e26542", "x_d8fdd83d", "x_854e2f53", "x_8cdaf2fa"]
urls = ["http://njdt.8684.cn/%s" % line for line in lines]
stations_file = 'stations.csv'
times_file = 'time.csv'
stations_header = ['station_name', 'number']
times_header = ['line', 'from_station', 'to_station', 'first_time', 'last_time']
get_all_lines_time()
