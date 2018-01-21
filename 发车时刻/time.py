import urllib.request
import json
import csv

# 将 dict 类型数据写入 CSV 文件
def write_csv_row(path_to_file, fieldnames, row):
    with open(path_to_file, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(row)

#获取高德地图的地铁站点信息，解析返回的json数据，保存到station.csv
def get_json(url,city):
    html = urllib.request.urlopen(url)
    hjson = json.loads(html.read().decode("utf-8"))

    #打开文件，设置表头
    with open("time_"+city+".csv", 'w') as csvfile:       #文件名为“time_BeiJing.csv”
        writer = csv.DictWriter(csvfile, fieldnames=stations_header)
        writer.writeheader()
    print(city)
    for i in range(len(hjson['l'])):   #遍历每一条线路
        ljson = hjson['l'][i]    #获取每条线路的json内容
        line_id = ljson['ls']
        for j in range(len(ljson['st'])):  #遍历每个站点
            station_id = ljson['st'][j]['si']  #站点编码（高德的编号）
            times = []
            for k in range(len( ljson['st'][j]['d'])):  ###处理站点的两个方向
                if line_id == ljson['st'][j]['d'][k]['ls']:
                  
                    djson = ljson['st'][j]['d'][k]
                    first_time= djson['ft']
                    end_name = djson['lt']
                    time = [first_time,end_name]
                    times.append(time)  
            if len(times)==1:             #有些地铁站只有从a到b的方向经过，b到a的方向不经过。
                    time = ['--:--','--:--']   #设置第2个方向的首班车和末班车时间为空
                    times.append(time)
            if len(times)==0:             #有些地铁站没开通，暂无首班车和末班车
                    time = ['--:--','--:--']   #设置第1个方向的首班车和末班车时间为空
                    times.append(time)
                    time = ['--:--','--:--']   #设置第2个方向的首班车和末班车时间为空
                    times.append(time)
            row ={'line_id':line_id,'station_id':station_id,'first_time':times[0][0],'end_name':times[0][1], 'first_time2':times[1][0],'end_name2':times[1][1]}
            write_csv_row("time_"+city+".csv", stations_header, row)


stations_header = ['line_id','station_id','first_time','end_name', 'first_time2','end_name2']

###########30个json的网址##########
urls = ['http://map.amap.com/service/subway?_1469083453980&srhdata=1100_info_beijing.json',
       'http://map.amap.com/service/subway?_1469083453980&srhdata=3100_info_shanghai.json',
       'http://map.amap.com/service/subway?_1469083453980&srhdata=4401_info_guangzhou.json',
       'http://map.amap.com/service/subway?_1469083453980&srhdata=4403_info_shenzhen.json',
       'http://map.amap.com/service/subway?_1469083453980&srhdata=4201_info_wuhan.json',
       'http://map.amap.com/service/subway?_1469083453980&srhdata=1200_info_tianjin.json',
       'http://map.amap.com/service/subway?_1469083453980&srhdata=3201_info_nanjing.json',

       'http://map.amap.com/service/subway?_1469083453980&srhdata=8100_info_xianggang.json',
       'http://map.amap.com/service/subway?_1469083453980&srhdata=5000_info_chongqing.json',
       'http://map.amap.com/service/subway?_1469083453980&srhdata=3301_info_hangzhou.json',
       'http://map.amap.com/service/subway?_1469083453980&srhdata=2101_info_shenyang.json',
       'http://map.amap.com/service/subway?_1469083453980&srhdata=2102_info_dalian.json',
       'http://map.amap.com/service/subway?_1469083453980&srhdata=5101_info_chengdu.json',
       'http://map.amap.com/service/subway?_1469083453980&srhdata=2201_info_changchun.json',

       'http://map.amap.com/service/subway?_1469083453980&srhdata=3205_info_suzhou.json',
       'http://map.amap.com/service/subway?_1469083453980&srhdata=4406_info_foshan.json',
       'http://map.amap.com/service/subway?_1469083453980&srhdata=5301_info_kunming.json',
       'http://map.amap.com/service/subway?_1469083453980&srhdata=6101_info_xian.json',
       'http://map.amap.com/service/subway?_1469083453980&srhdata=4101_info_zhengzhou.json',
       'http://map.amap.com/service/subway?_1469083453980&srhdata=4301_info_changsha.json',
       'http://map.amap.com/service/subway?_1469083453980&srhdata=3302_info_ningbo.json',

       'http://map.amap.com/service/subway?_1469083453980&srhdata=3202_info_wuxi.json',
       'http://map.amap.com/service/subway?_1469083453980&srhdata=3702_info_qingdao.json',
       'http://map.amap.com/service/subway?_1469083453980&srhdata=3601_info_nanchang.json',
       'http://map.amap.com/service/subway?_1469083453980&srhdata=3501_info_fuzhou.json',
       'http://map.amap.com/service/subway?_1469083453980&srhdata=4419_info_dongguan.json',
       'http://map.amap.com/service/subway?_1469083453980&srhdata=4501_info_nanning.json',
       'http://map.amap.com/service/subway?_1469083453980&srhdata=3401_info_hefei.json',
        
       'http://map.amap.com/service/subway?_1469083453980&srhdata=2301_info_haerbin.json',
       'http://map.amap.com/service/subway?_1469083453980&srhdata=1301_info_shijiazhuang.json',
        ]

###########30个城市的名字##########
city = ['BeiJing','ShangHai','GuangZhou','ShenZhen','WuHan','TianJin','NanJing',
        'XiangGang','ChongQin','HangZhou','ShenYang','DaLian','ChengDu','ChangChun',
        'SuZhou','FoShan','KunMing','XiAn','ZhengZhou','ChangSha','NingBo',
        'WuXi','QingDao','NanChang','FuZhou','DongGuan','NanNing','HeFei',
        'HaErbin','ShiJiazhuang'
        ]
for i in range(len(urls)):          #处理每一个网址
    get_json(urls[i],city[i])       #传递网址和城市名字
