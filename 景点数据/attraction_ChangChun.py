#!/usr/bin/python
# -*- coding:utf-8 -*-

#date :2017.4.20
#test csv读取到字典list_jingdian,读取字典list_jiandian获取景点名称，并获取其详细信息。再查询其距离最近的地铁站

import csv
import json
import time
import json
import urllib
from urllib import request
import sys
from urllib.parse import quote
import codecs
import xml.etree.ElementTree as ET
import xml.dom.minidom
import pprint
import traceback



def read_csv(filename):  #读取 旅游局星级景点名录 .csv。转换为列表list_jingdian,其中为景点 集合。
    list_jingdian = []
    with open(filename,'r',encoding='gbk') as csvfile:
        reader = csv.DictReader(csvfile)
       
        for row in reader:
            d={}
            d["序号"] = row['序号']
            d["景区名称"]= row['单位']
            if row['星级'] =='5A':
                d["星级"] = 5
            if row['星级'] =='4A':
                d["星级"] = 4
            if row['星级'] =='3A':
                d["星级"] = 3
            if row['星级'] =='2A':
                d["星级"] = 2
            if row['星级'] =='1A':
                d["星级"] = 1

            d["地址"] = row['地址']
            list_jingdian.append(d)
    return list_jingdian

def get_roundsearch(query,lat,lng,radius,ak_KEY):  #检索 经纬度（lat,lng)为圆心，radius为半径，query关键词，并返回离圆心 驾车，骑行，步行，最近的query
    url = 'http://api.map.baidu.com/place/v2/search?query='+ quote(query)+'&location='+ str(lat) +','+ str(lng) + '&radius='+str(radius)+'&output=xml&ak=' + ak_KEY
    xml_obj = request.urlopen(url)
    data = xml_obj.read()
    xml_obj.close
    root =  ET.fromstring(data) #同上一句   tree =  ET.ElementTree(file = 't1.xml')
    subway_list = []  #用于存放景点附近的地铁站信息
    subway_list_new = []
    
    try:
       if root[2].find('result') is None:
            print("none")

       else:
            item = root.find('results').findall('result')[0]
            d = {}
            d["name"] = item.find('name').text
            d["line"] = item.find('address').text
            loc = item.find('location')
            d["lat"] = loc.find('lat').text
            d["lng"] = loc.find('lng').text
            #***********以下为获取地铁站 到 该景点的 距离*************
           
            walking  = "walking"
            dis = distance(walking,lat,lng,d["lat"],d["lng"])
            if dis is not None: #获取 步行距离
                d["distance_walking"] = dis[0]    #距离
                d['duration_walking'] = dis[1]    #时间
         
            subway_list.append(d)
    except:
        traceback.print_exc()
        print(root)
       

    return [subway_list]

def distance(way,origin_lat,origin_lng,destination_lat,destination_lng):  #返回起终点（origin_lat,origin_lng),(destination_lat,destination_lng之间的步行距离。way 可选择drving(驾车)，riding（骑行），walking（步行）

    url = 'http://api.map.baidu.com/routematrix/v2/'+str(way)+'?output=json&origins='+str(origin_lat)+','+str(origin_lng) +'&destinations='+ str(destination_lat)+','+str(destination_lng)+ '&ak=' + ak_KEY   
    json_obj2 = request.urlopen(url)
    data = json.load(json_obj2)  #json转换为字典dic
   # print(url)
     
    item2 = data["result"][0]
    jdistance_value = item2["distance"]["value"]
    jduration_value = item2["duration"]["value"]
    return [jdistance_value,jduration_value]

if __name__ == '__main__':
    print ("start..")
    start_time = time.time()
    num = 0

    #ak_KEY = 'XvClGa7UfyuLHow7huftkGjLHVgFtyBn'  #  (test) 在此修改 百度地图 AK密钥
    #ak_KEY = 'riuQcTzlOfPDIxWlxf2GYxmE2Iz3AriY'  #  (mingming)
    #ak_KEY =  'Sz7tY8SBXh5zi0lnIlfH4u9KLKUn6A0g'  #  (youming)
    ak_KEY ='lGVFAnRfsGYLYsh2Dt9TtGRgkLzA7prH'     #(JiangQun)

    outfile_name = 'attraction_ChangChun.json' #在此修改 输出文件名字
    csv_name = '长春市景点.csv'  #在此修改 旅游局星级景点名录,需要”ID",""景区名称”，”星级“，“地址”，“详细介绍”五列
    list_jingdian = read_csv(csv_name)
    #print (list_jingdian)

    city_name = '长春'  #在此修改景点所在城市名
    city_id = '220100' #在此修改省份城市编码


    doc = codecs.open(outfile_name,'w','utf-8')
    count = 1
    no_find_jingdian = []   #用于存放 未检索到的景点名
    outfile2='长春市景点(无).csv'
    header = ['序号','景区名称','星级','地址']
    #打开文件，设置表头
    with open(outfile2, 'w') as csvfile:       
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
    
    for jd in list_jingdian:
        jingdian_name = jd["景区名称"]

        url = 'http://api.map.baidu.com/place/v2/search?query='+ quote(jingdian_name)+ '&region='+ quote(city_name) +'&city_limit=true&page_size=1&page_num=0&scope=2&output=json&ak='+ak_KEY
        
        json_obj = request.urlopen(url)
        data = json.load(json_obj)  #json转换为字典dic
    
        print(jingdian_name)
        time.sleep(2) # 休眠1秒
        jingdian = {} #一个市的景点的dict
    
       
        if data["results"] == []:    #如果百度地图没有检索到此景点，存入新的文件等待第二次处理
            with open(outfile2, 'a') as csvfile:
                writer = csv.DictWriter(csvfile,header)
                writer.writerow(jd)
        else:
            item = data["results"][0]
            # print("{:0>4d}".format(count))
            # print(type("{:0>4d}".format(count)))
            jingdian["id"] =  str(city_id)+ "{:0>3d}".format(count)
            count += 1 #编号自加1
            jingdian["name"] = item["name"]
            jingdian["level"] = jd['星级']
            jingdian["address"] = jd['地址']
            jingdian["lat"] = item["location"]["lat"]
            jingdian["lng"] = item["location"]["lng"]
            jingdian["uid"] = item["uid"]
          
            if "detail_info" in item and 'tag' in  item["detail_info"]: #因为有些景点无tag，所以要先判断。
               jingdian["tag"] =  item["detail_info"]["tag"]
            else:
               jingdian["tag"] = '无'


            #**********以下为 圆形搜索 景点附近5000米内 地铁站*
            query = '地铁站'
            radius = 2000   #搜索半径为1000米
            subway = get_roundsearch(query,jingdian["lat"],jingdian["lng"],radius,ak_KEY)[0] #景点附近最近的地铁站
            if subway != []:
                jingdian["subway"] = subway
        
            jingdian = json.dumps(jingdian,ensure_ascii=False)
            #jingdian = json.dumps(jingdian,ensure_ascii=False,indent = 2)  #有缩进，Jason更好看

            doc.write(jingdian)
            doc.write('\n')   
       
    doc.close()
    end_time = time.time()
    print ("spending time %.2fs" % (end_time - start_time))
