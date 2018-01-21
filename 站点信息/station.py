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
    with open("stations_"+city+".csv", 'w') as csvfile:       #文件名为“stations_BeiJing.csv”
        writer = csv.DictWriter(csvfile, fieldnames=stations_header)
        writer.writeheader()
      
    city_name = hjson['s'] #城市名称
    number = 1
    station_names = {}
    for i in range(len(hjson['l'])):   #遍历每一条线路
        ljson = hjson["l"][i]    #获取每条线路的json内容
        line = ljson['ln']       #解析线路名称
        line_id = ljson['ls']
        for j in range(len(ljson['st'])):  #遍历每个站点
            station_name = ljson['st'][j]['n']  #站点名称
            station_id = ljson['st'][j]['sid']  #站点编码（高德的编号）
            langengrad = ljson['st'][j]['sl']  #站点经纬度（高德的经纬度）
            state = ljson['st'][j]['su']  #站点运营状态（1表示可用，3表示正在建设）

             #####给每个唯一的站点编上序号##
            if station_name in station_names:
                 continue
            else:          
                station_names[station_name] = number
                row ={'city':city_name,'line':line,'line_id':line_id,'station_name':station_name, 'station_id':station_id,'langengrad':langengrad,'state':state,'counter':number}
                write_csv_row("stations_"+city+".csv", stations_header, row)
                number += 1


stations_file = 'stations.csv'
stations_header = ['city','line','line_id','station_name', 'station_id','langengrad','state','counter']
urls = ['http://map.amap.com/service/subway?_1469083453978&srhdata=1100_drw_beijing.json',
       'http://map.amap.com/service/subway?_1469083453978&srhdata=3100_drw_shanghai.json',
       'http://map.amap.com/service/subway?_1469083453978&srhdata=4401_drw_guangzhou.json',
       'http://map.amap.com/service/subway?_1469083453978&srhdata=4403_drw_shenzhen.json',
       'http://map.amap.com/service/subway?_1469083453978&srhdata=4201_drw_wuhan.json',
       'http://map.amap.com/service/subway?_1469083453978&srhdata=1200_drw_tianjin.json',
       'http://map.amap.com/service/subway?_1469083453978&srhdata=3201_drw_nanjing.json',

       'http://map.amap.com/service/subway?_1469083453978&srhdata=8100_drw_xianggang.json',
       'http://map.amap.com/service/subway?_1469083453978&srhdata=5000_drw_chongqing.json',
       'http://map.amap.com/service/subway?_1469083453978&srhdata=3301_drw_hangzhou.json',
       'http://map.amap.com/service/subway?_1469083453978&srhdata=2101_drw_shenyang.json',
       'http://map.amap.com/service/subway?_1469083453978&srhdata=2102_drw_dalian.json',
       'http://map.amap.com/service/subway?_1469083453978&srhdata=5101_drw_chengdu.json',
       'http://map.amap.com/service/subway?_1469083453978&srhdata=2201_drw_changchun.json',

       'http://map.amap.com/service/subway?_1469083453978&srhdata=3205_drw_suzhou.json',
       'http://map.amap.com/service/subway?_1469083453978&srhdata=4406_drw_foshan.json',
       'http://map.amap.com/service/subway?_1469083453978&srhdata=5301_drw_kunming.json',
       'http://map.amap.com/service/subway?_1469083453978&srhdata=6101_drw_xian.json',
       'http://map.amap.com/service/subway?_1469083453978&srhdata=4101_drw_zhengzhou.json',
       'http://map.amap.com/service/subway?_1469083453978&srhdata=4301_drw_changsha.json',
       'http://map.amap.com/service/subway?_1469083453978&srhdata=3302_drw_ningbo.json',

       'http://map.amap.com/service/subway?_1469083453978&srhdata=3202_drw_wuxi.json',
       'http://map.amap.com/service/subway?_1469083453978&srhdata=3702_drw_qingdao.json',
       'http://map.amap.com/service/subway?_1469083453978&srhdata=3601_drw_nanchang.json',
       'http://map.amap.com/service/subway?_1469083453978&srhdata=3501_drw_fuzhou.json',
       'http://map.amap.com/service/subway?_1469083453978&srhdata=4419_drw_dongguan.json',
       'http://map.amap.com/service/subway?_1469083453978&srhdata=4501_drw_nanning.json',
       'http://map.amap.com/service/subway?_1469083453978&srhdata=3401_drw_hefei.json',
        
       'http://map.amap.com/service/subway?_1469083453978&srhdata=2301_drw_haerbin.json',
       'http://map.amap.com/service/subway?_1469083453978&srhdata=1301_drw_shijiazhuang.json',
        ]

###########30个城市的名字##########
city = ['BeiJing','ShangHai','GuangZhou','ShenZhen','WuHan','TianJin','NanJing',
        'XiangGang','ChongQin','HangZhou','ShenYang','DaLian','ChengDu','ChangChun',
        'SuZhou','FoShan','KunMing','XiAn','ZhengZhou','ChangSha','NingBo',
        'WuXi','QingDao','NanChang','FuZhou','DongGuan','NanNing','HeFei',
        'HaErbin','ShiJiazhuang'
        ]
for i in range(len(urls)):
    get_json(urls[i],city[i])
