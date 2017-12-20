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
    elif  "："in time:
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
    with open(times_file2, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=times_header2)
        writer.writeheader()
    with open(stations_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=stations_header)
        writer.writeheader()
    for url in urls:
        get_one_line_time(url)      #获取所有线路的数据
        
def get_one_line_time(url):
    html = get_html(url)     #获取html页面
    bsobj = BeautifulSoup(html, "lxml")       #用lxml解析html
    tbody = bsobj.findAll("tbody")    #查找到显示线路信息的表格
    while tbody is None:
        print("        retry ...")
        html = get_html(url)
        bsobj = BeautifulSoup(html, "lxml")
        tbody = bsobj.findAll("tbody")    #查找到显示线路信息的表格

    global number
    global station_names   #326

    ###########处理1号线#############
    trs = tbody[0].findAll("tr")        #把所有行放入数组trs[]
    stations = []
    for tr in trs:                     #开始遍历每一行
        tds = tr.findAll("td")         #把一行中的所有列放入数组tds[]
        th  =tr.find("th")
        line = 1
        station_name = th.get_text()
        toStart_time = minutes(tds[0].get_text())  #方向1首班车时间
        toEnd_time = minutes(tds[1].get_text())    #方向1末班车时间
        toStart_time2 = minutes(tds[3].get_text())   #方向2首班车时间
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
    
    for i in range(n-1):
        row = { "line": line, "from_station": stations[i][1], "to_station": stations[i+1][1], "first_time": stations[i][2], "last_time": stations[i][3],}
        write_csv_row(times_file, times_header, row)
        ########周五延长1号线末班车时间，上行（开往四惠东方向）末班车延长35分钟########
        row = { "line": line, "from_station": stations[i][1], "to_station": stations[i+1][1], "first_time": stations[i][2], "last_time": int(stations[i][3])+35,}
        write_csv_row(times_file2, times_header2, row)
    for i in range(n-1):    
        row = { "line": line, "from_station": stations[i+1][1], "to_station": stations[i][1], "first_time": stations[i+1][4], "last_time": stations[i+1][5],}
        write_csv_row(times_file, times_header, row)
        ######## 下行（开往苹果园方向）末班车延长15分钟########
        row = { "line": line, "from_station": stations[i+1][1], "to_station": stations[i][1], "first_time": stations[i+1][4],"last_time": int(stations[i+1][5])+15,}
        write_csv_row(times_file2, times_header2, row)

    ###########处理2号线#############
    trs = tbody[1].findAll("tr")        #把所有行放入数组trs[]
    stations = []
    for tr in trs:                     #开始遍历每一行
        tds = tr.findAll("td")         #把一行中的所有列放入数组tds[]
        th  =tr.find("th")
        line = "2"
        station_name = th.get_text()
        toStart_time = minutes(tds[0].get_text())  #方向1首班车时间
        toEnd_time = minutes(tds[1].get_text())    #方向1末班车时间
        toStart_time2 = minutes(tds[3].get_text())   #方向2首班车时间
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
  
    for i in range(n-1):      #外环
        row = { "line": line+"(外环)", "from_station": stations[i+1][1], "to_station": stations[i][1], "first_time": stations[i+1][2], "last_time": stations[i+1][3],}
        write_csv_row(times_file, times_header, row)
    row = { "line": line+"(外环)", "from_station": stations[0][1], "to_station": stations[n-1][1], "first_time": stations[0][2], "last_time": stations[0][3],}
    write_csv_row(times_file, times_header, row)  
    
    for i in range(1,n-1):    #内环
        row = { "line": line+"(内环)", "from_station": stations[i][1], "to_station": stations[i+1][1], "first_time": stations[i][4], "last_time": stations[i][5],}
        write_csv_row(times_file, times_header, row)
    row = { "line": line+"(内环)", "from_station": stations[n-1][1], "to_station": stations[0][1], "first_time": stations[n-1][4], "last_time": stations[n-1][5],}
    write_csv_row(times_file, times_header, row)
    row = { "line": line+"(内环)", "from_station": stations[0][1], "to_station": stations[1][1], "first_time": stations[0][4], "last_time": stations[0][5],}
    write_csv_row(times_file, times_header, row)

     ###########处理4号线#############
    line = 4
    trs = tbody[2].findAll("tr")
    stations = []
    for tr in trs:                         #开始遍历每一行
        tds = tr.findAll("td")         #把一行中的所有列放入数组tds[]
        th  =tr.findAll("th")
        station_name = th[0].get_text()
        station_name2 = th[1].get_text()
        toStart_time = minutes(tds[0].get_text())   #方向1首班车时间
        toEnd_time = minutes(tds[1].get_text())     #方向1末班车时间
        toStart_time2 = minutes(tds[2].get_text())   #方向2首班车时间
        if tds[4].get_text()=="——":
            toEnd_time2 = minutes(tds[3].get_text())     #方向2末班车时间
        else:
            toEnd_time2 = minutes(tds[4].get_text())     #方向2末班车时间
        station = [line, station_name, toStart_time, toEnd_time, toStart_time2, toEnd_time2,station_name2]
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
    for i in range(n-1):      #方向1
         row = { "line": line, "from_station": stations[i][1], "to_station": stations[i+1][1], "first_time": stations[i][2], "last_time": stations[i][3],}
         write_csv_row(times_file, times_header, row)
    for i in range(n-1):      #方向2
         row = { "line": line, "from_station": stations[i][6], "to_station": stations[i+1][6], "first_time": stations[i][4], "last_time": stations[i][5],}
         write_csv_row(times_file, times_header, row)

    ###########处理6号线#############
    line = 6
    trs = tbody[4].findAll("tr")
    stations = []
    for tr in trs:                         #开始遍历每一行
        tds = tr.findAll("td")         #把一行中的所有列放入数组tds[]
        th  =tr.find("th")
        station_name = th.get_text()
        toStart_time = minutes(tds[0].get_text())   #方向1首班车时间
        toEnd_time = minutes(tds[1].get_text())     #方向1末班车时间
        toStart_time2 = minutes(tds[2].get_text())   #方向2首班车时间
        if ":" not in  tds[4].get_text():
            toEnd_time2 = minutes(tds[3].get_text())     #方向2末班车时间
        else:
            toEnd_time2 = minutes(tds[4].get_text())     #方向2末班车时间
        station = [line, station_name, toStart_time, toEnd_time, toStart_time2, toEnd_time2]
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
    for i in range(n-1):      #方向1
         row = { "line": line, "from_station": stations[i+1][1], "to_station": stations[i][1], "first_time": stations[i+1][2], "last_time": stations[i+1][3],}
         write_csv_row(times_file, times_header, row)
    for i in range(n-1):      #方向2
         row = { "line": line, "from_station": stations[i][1], "to_station": stations[i+1][1], "first_time": stations[i][4], "last_time": stations[i][5],}
         write_csv_row(times_file, times_header, row)

   ###########处理5、8、八通、亦庄线#############
 
    lines = [5,8,"八通线","亦庄线"]
    array = [tbody[3].findAll("tr"),tbody[6].findAll("tr"),tbody[14].findAll("tr"),tbody[16].findAll("tr")]
    for i in range(len(lines)):
        line = lines[i]
        stations = []
        for tr in array[i]:                     #开始遍历每一行
            tds = tr.findAll("td")         #把一行中的所有列放入数组tds[]
            th  =tr.find("th")
            station_name = th.get_text()
            toStart_time = minutes(tds[0].get_text())  #方向1首班车时间
            toEnd_time = minutes(tds[1].get_text())    #方向1末班车时间
            toStart_time2 = minutes(tds[2].get_text())   #方向2首班车时间
            toEnd_time2 = minutes(tds[3].get_text())     #方向2末班车时间
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
        for i in range(n-1):      #方向1
            row = { "line": line, "from_station": stations[i][1], "to_station": stations[i+1][1], "first_time": stations[i][2], "last_time": stations[i][3],}
            write_csv_row(times_file, times_header, row)
        for i in range(n-1):      #方向2
            row = { "line": line, "from_station": stations[i+1][1], "to_station": stations[i][1], "first_time": stations[i+1][4], "last_time": stations[i+1][5],}
            write_csv_row(times_file, times_header, row)
            
     ###########处理7,9号线#############
 
    lines = [7,9]
    array = [tbody[5].findAll("tr"),tbody[7].findAll("tr")]
    for i in range(len(lines)):
        line = lines[i]
        stations = []
        for tr in array[i]:                     #开始遍历每一行
            tds = tr.findAll("td")         #把一行中的所有列放入数组tds[]
            th  =tr.find("th")
            station_name = th.get_text()
            toStart_time = minutes(tds[0].get_text())   #方向1首班车时间
            toEnd_time = minutes(tds[1].get_text())     #方向1末班车时间
            toStart_time2 = minutes(tds[2].get_text())   #方向2首班车时间
            toEnd_time2 = minutes(tds[3].get_text())     #方向2末班车时间
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
        for i in range(n-1):      #方向1
             row = { "line": line, "from_station": stations[i+1][1], "to_station": stations[i][1], "first_time": stations[i+1][2], "last_time": stations[i+1][3],}
             write_csv_row(times_file, times_header, row)
        for i in range(n-1):      #方向2
             row = { "line": line, "from_station": stations[i][1], "to_station": stations[i+1][1], "first_time": stations[i][4], "last_time": stations[i][5],}
             write_csv_row(times_file, times_header, row)


    ###########处理10号线#############
    line = "10"
    trs = tbody[8].findAll("tr")
    stations = []
    for tr in trs:                         #开始遍历每一行
        tds = tr.findAll("td")         #把一行中的所有列放入数组tds[]
        th  =tr.findAll("th")
        station_name = th[0].get_text()
        station_name2 = th[1].get_text()
        toStart_time = minutes(tds[0].get_text())   #方向1首班车时间
        toEnd_time = minutes(tds[1].get_text())     #方向1末班车时间
        toStart_time2 = minutes(tds[4].get_text())   #方向2首班车时间
        toEnd_time2 = minutes(tds[5].get_text())     #方向2末班车时间
        station = [line, station_name, toStart_time, toEnd_time, toStart_time2, toEnd_time2,station_name2]
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
    #方向1,单独处理后面三个站
    row = { "line": line+"(内环)", "from_station": stations[n-3][1], "to_station": stations[n-2][1], "first_time": stations[n-3][2], "last_time": stations[n-3][3],}
    write_csv_row(times_file, times_header, row)
    row = { "line": line+"(内环)", "from_station": stations[n-2][1], "to_station": stations[n-1][1], "first_time": stations[n-2][2], "last_time": stations[n-2][3],}
    write_csv_row(times_file, times_header, row)
    row = { "line": line+"(内环)", "from_station": stations[n-1][1], "to_station": stations[0][1], "first_time": stations[n-1][2], "last_time": stations[n-1][3],}
    write_csv_row(times_file, times_header, row)
    
    for i in range(n-3):      #方向1,留出后面三个站
         row = { "line": line+"(外环)", "from_station": stations[i][1], "to_station": stations[i+1][1], "first_time": stations[i][2], "last_time": stations[i][3],}
         write_csv_row(times_file, times_header, row)
    for i in range(n-1):      #方向2
         row = { "line": line+"(外环)", "from_station": stations[i+1][6], "to_station": stations[i][6], "first_time": stations[i+1][4], "last_time": stations[i+1][5],}
         write_csv_row(times_file, times_header, row)
            
    row = { "line": line+"(外环)", "from_station": stations[0][6], "to_station": stations[n-1][6], "first_time": stations[0][4], "last_time": stations[0][5],}
    write_csv_row(times_file, times_header, row)    
   ###########处理13号线#############
    line = 13
    trs = tbody[9].findAll("tr")
    stations = []
    for tr in trs:                         #开始遍历每一行
        tds = tr.findAll("td")         #把一行中的所有列放入数组tds[]
        th  =tr.find("th")
        station_name = th.get_text()
        toStart_time = minutes(tds[0].get_text())   #方向1首班车时间
        if ":" not in  tds[5].get_text():
            toEnd_time = minutes(tds[2].get_text())     #方向1末班车时间
        else:
            toEnd_time = minutes(tds[5].get_text())    #方向1末班车时间
            
        toStart_time2 = minutes(tds[1].get_text())   #方向2首班车时间
        if ":" not in  tds[4].get_text():
            toEnd_time2 = minutes(tds[3].get_text())     #方向2末班车时间
        else:
            toEnd_time2 = minutes(tds[4].get_text())     #方向2末班车时间
        station = [line, station_name, toStart_time, toEnd_time, toStart_time2, toEnd_time2]
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
    for i in range(n-1):      #方向1
         row = { "line": line, "from_station": stations[i+1][1], "to_station": stations[i][1], "first_time": stations[i+1][2], "last_time": stations[i+1][3],}
         write_csv_row(times_file, times_header, row)
    for i in range(n-1):      #方向2
         row = { "line": line, "from_station": stations[i][1], "to_station": stations[i+1][1], "first_time": stations[i][4], "last_time": stations[i][5],}
         write_csv_row(times_file, times_header, row)

    ###########处理14号线#############
    lines = ["14(西段)","14(东段)"]
    trs = [tbody[10].findAll("tr"),tbody[11].findAll("tr")]

    for i in range(2):
        stations = []
        line = lines[i]
        for tr in trs[i]:                         #开始遍历每一行
            tds = tr.findAll("td")         #把一行中的所有列放入数组tds[]
            th  =tr.find("th")
            station_name = th.get_text()
            toStart_time = minutes(tds[0].get_text())   #方向1首班车时间
            toEnd_time = minutes(tds[1].get_text())    #方向1末班车时间
            
            toStart_time2 = minutes(tds[2].get_text())   #方向2首班车时间
            if(i==0):
                if ":" not in  tds[4].get_text():
                    toEnd_time2 = minutes(tds[3].get_text())     #方向2末班车时间
                else:
                    toEnd_time2 = minutes(tds[4].get_text())    #方向2末班车时间
            else:
                toEnd_time2 = minutes(tds[3].get_text())     #方向2末班车时间
            station = [line, station_name, toStart_time, toEnd_time, toStart_time2, toEnd_time2]
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
        for i in range(n-1):      #方向1
             row = { "line": line, "from_station": stations[i][1], "to_station": stations[i+1][1], "first_time": stations[i][2], "last_time": stations[i][3],}
             write_csv_row(times_file, times_header, row)
        for i in range(n-1):      #方向2
             row = { "line": line, "from_station": stations[i+1][1], "to_station": stations[i][1], "first_time": stations[i+1][4], "last_time": stations[i+1][5],}
             write_csv_row(times_file, times_header, row)
         

    ###########处理15号线#############
    line = 15
    trs = tbody[12].findAll("tr")
    stations = []
    for tr in trs:                         #开始遍历每一行
        tds = tr.findAll("td")         #把一行中的所有列放入数组tds[]
        th  =tr.find("th")
        station_name = th.get_text()
        toStart_time = minutes(tds[0].get_text())   #方向1首班车时间
        if ":" not in  tds[2].get_text():
            toEnd_time = minutes(tds[1].get_text())     #方向1末班车时间
        else:
            toEnd_time = minutes(tds[2].get_text())    #方向1末班车时间
            
        toStart_time2 = minutes(tds[3].get_text())   #方向2首班车时间
        toEnd_time2 = minutes(tds[4].get_text())     #方向2末班车时间
        station = [line, station_name, toStart_time, toEnd_time, toStart_time2, toEnd_time2]
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
    for i in range(n-1):      #方向1
         row = { "line": line, "from_station": stations[i][1], "to_station": stations[i+1][1], "first_time": stations[i][2], "last_time": stations[i][3],}
         write_csv_row(times_file, times_header, row)
    for i in range(n-1):      #方向2
         row = { "line": line, "from_station": stations[i+1][1], "to_station": stations[i][1], "first_time": stations[i+1][4], "last_time": stations[i+1][5],}
         write_csv_row(times_file, times_header, row)


    ###########处理昌平线#############
    line = "昌平线"
    trs = tbody[15].findAll("tr")
    stations = []
    for tr in trs:                         #开始遍历每一行
        tds = tr.findAll("td")         #把一行中的所有列放入数组tds[]
        th  =tr.find("th")
        station_name = th.get_text()
        toStart_time = minutes(tds[0].get_text())   #方向1首班车时间
        if ":" not in  tds[3].get_text():
            toEnd_time = minutes(tds[2].get_text())     #方向1末班车时间
        else:
            toEnd_time = minutes(tds[3].get_text())    #方向1末班车时间
            
        toStart_time2 = minutes(tds[1].get_text())   #方向2首班车时间
        toEnd_time2 = minutes(tds[4].get_text())     #方向2末班车时间
        station = [line, station_name, toStart_time, toEnd_time, toStart_time2, toEnd_time2]
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
    for i in range(n-1):      #方向1
         row = { "line": line, "from_station": stations[i][1], "to_station": stations[i+1][1], "first_time": stations[i][2], "last_time": stations[i][3],}
         write_csv_row(times_file, times_header, row)
    for i in range(n-1):      #方向2
         row = { "line": line, "from_station": stations[i+1][1], "to_station": stations[i][1], "first_time": stations[i+1][4], "last_time": stations[i+1][5],}
         write_csv_row(times_file, times_header, row)
             
number = 1
station_names ={}
urls = ["http://www.bjsubway.com/e/action/ListInfo/?classid=39&ph=1"]
stations_file = 'stations.csv'
times_file = 'time.csv'
times_file2 = 'time_friday.csv'
stations_header = ['station_name', 'number']
times_header = ['line', 'from_station', 'to_station', 'first_time', 'last_time']
times_header2 = ['line', 'from_station', 'to_station', 'first_time', 'last_time']
get_all_lines_time()
