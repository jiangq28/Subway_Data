#coding=utf-8
import json
import xml.etree.ElementTree as ET
import xml.dom.minidom
import pprint
import time
import csv
import codecs
from urllib.parse import quote
import urllib
from urllib import request
import sys
import importlib
importlib.reload(sys)



def get_detail(result,uid,ak_KEY):  #获取景点营业时间和简介，分别写入 字典 result["shop_hours"]和 result["description"]
    url_detail = 'http://api.map.baidu.com/place/v2/detail?uid=' + uid + '&output=json&scope=2&ak=' + ak_KEY  #访问详细介绍
    json_detailobj = request.urlopen(url_detail)
    data_detail = json.load(json_detailobj)# json 转换dict
    #item1 = data_detail["result"]

    if "result" in data_detail and '旅游景点' in data_detail["result"]["detail_info"]["tag"]: #判断是否属于旅游景点
        result["tag"]=  data_detail["result"]["detail_info"]["tag"]
        return 1
    return 0  #过滤掉不属于景点的地方

def distance(way,origin_lat,origin_lng,destination_lat,destination_lng,ak_KEY):  #返回起终点（origin_lat,origin_lng),(destination_lat,destination_lng之间的步行距离。way 可选择drving(驾车)，riding（骑行），walking（步行）

    url = 'http://api.map.baidu.com/routematrix/v2/'+str(way)+'?output=json&origins='+str(origin_lat)+','+str(origin_lng) +'&destinations='+ str(destination_lat)+','+str(destination_lng)+ '&ak=' + ak_KEY
    #url = 'http://api.map.baidu.com/routematrix/v2/walking?output=json&origins=23.078618,113.411678&destinations=23.064521,113.391927&ak=XvClGa7UfyuLHow7huftkGjLHVgFtyBn'

    json_obj2 = request.urlopen(url)
    data = json.load(json_obj2)  #json转换为字典dic

    for item2 in data["result"]:
        jdistance_value = item2["distance"]["value"]
    return jdistance_value


def get_roundsearch(query,lat,lng,radius,ak_KEY):  #检索 经纬度（lat,lng)为圆心，radius为半径，query关键词，并返回离圆心 驾车，骑行，步行，最近的query
    url = 'http://api.map.baidu.com/place/v2/search?query='+ quote(query)+'&location='+ str(lat) +','+ str(lng) + '&radius='+str(radius)+'&output=xml&ak=' + ak_KEY
    xml_obj = request.urlopen(url)
    data = xml_obj.read()
    xml_obj.close

    root =  ET.fromstring(data) #同上一句   tree =  ET.ElementTree(file = 't1.xml')
    subway_list = []  #用于存放景点附近 所有 地铁站
    global subway_list_new #用于存放 驾车，骑行，步行，最近的地铁站
    subway_list_new = []

    if root is None:
        print("none")
    elif root[2].find('result') is None:
        print("none")
    else:
        item = root.find('results').findall('result')[0]
        d = {}
        d["name"] = item.find('name').text
        loc = item.find('location')
        d["lat"] = loc.find('lat').text
        d["lng"] = loc.find('lng').text

        #***********以下为获取地铁站 到 该景点的 距离*************
        walking  = "walking"
        if  distance(walking,lat,lng,d["lat"],d["lng"],ak_KEY) is not None: #获取 步行距离
            d["distance_walking"] = distance(walking,lat,lng,d["lat"],d["lng"],ak_KEY)
        else:
            d["distance_walking"] = 888888888
        subway_list.append(d)

        subway_list_new = []

        subway_walking = sorted(subway_list,key=lambda k: k['distance_walking'])  #将地铁站 根据 距离大小排序，距离越近的排在前面
        subway_walking_min = subway_walking[0]
        subway_list_new.append(subway_walking_min)

    return subway_list_new


def get_attract(city):
    #ak_KEY = 'XvClGa7UfyuLHow7huftkGjLHVgFtyBn'  #  (test) 在此修改 百度地图 AK密钥
    ak_KEY = 'riuQcTzlOfPDIxWlxf2GYxmE2Iz3AriY'  #  (mingming)
    #ak_KEY =  'Sz7tY8SBXh5zi0lnIlfH4u9KLKUn6A0g'  #  (youming)
    num = 0;         #请求20页，0~10
    url = "http://api.map.baidu.com/place/v2/search?query="+quote('景点')+"&region="+quote(city)+"&city_limit=true&page_size=20&page_num="+str(num)+"&output=json&ak="+ ak_KEY
    json_obj = request.urlopen(url)
    data = json.load(json_obj)  #json转换为字典dic
    count = 1       #计数景点的个数
    doc = codecs.open("attrction_" + city,'w','utf-8')
    
    city_id = '010' #在此修改省份城市编码
    while num < 20:    
      
        l = len(data["results"])
        print(l)
        for i in range(l):
            jingdian = {} #一个市的景点的dict
            item = data["results"][i]
             #****获取分类、 营业时间 与简介***********
            if get_detail(jingdian,item["uid"],ak_KEY):  #如果属于旅游景点
                jingdian["id"] =  str(city_id)+ "{:0>3d}".format(count)
                count += 1 #编号自加1
                jingdian["name"] = item["name"]
               # jingdian["level"] = jd['等级']
                jingdian["address"] = item['address']
                jingdian["lat"] = item["location"]["lat"]
                jingdian["lng"] = item["location"]["lng"]
                jingdian["uid"] = item["uid"]
                print (jingdian["name"])

                #**********以下为 圆形搜索 景点附近2000米内 地铁站*
                query = '地铁站'
                radius = 2000   #搜索半径为2000米

                jingdian["subway"] = get_roundsearch(query,jingdian["lat"],jingdian["lng"],radius,ak_KEY) #景点附近最近的地铁站
                jingdian = json.dumps(jingdian,ensure_ascii=False)
        #jingdian = json.dumps(jingdian,ensure_ascii=False,indent = 2)  #有缩进，Jason更好看
                doc.write(jingdian)
                doc.write('\n')
        url = "http://api.map.baidu.com/place/v2/search?query="+quote('景点')+"&region="+quote(city)+"&city_limit=true&page_size=20&page_num="+str(num)+"&output=json&ak="+ ak_KEY
        json_obj = request.urlopen(url)
        data = json.load(json_obj)  #json转换为字典dic

    doc.close()

  

if __name__ == '__main__':
    print ("start..")
    start_time = time.time()
    ###########30个城市的名字##########
    city = ['北京']
    for i in range(len(city)):
        get_attract(city[i])
    end_time = time.time()
    print ("spending time %.2fs" % (end_time - start_time))
    
