# -*- coding: utf-8 -*-

import pandas as pd
import urllib
import hashlib
from urllib import urlencode
import urllib2
import json
import io
import re
from itertools import groupby
import sys
from tqdm import tqdm
import codecs
reload(sys)
sys.setdefaultencoding('utf8')
# 以get请求为例http://api.map.baidu.com/geocoder/v2/?address=百度大厦&output=json&ak=yourak


# fzzp = pd.read_json("fzzp.json", orient='records')

lines = [line.rstrip('\n') for line in io.open('fzzp.json')]
# print lines[2]
# h=  lines[2]
# row = json.loads(h)
# print row['common']
api_list=[
    '26144bdf78ea521f67a4abac38ee23d4',
    '3e8d96c1d83993e93a5c6d06537013c3',
    '73b98849aed5fc5ac4260071f035bc74',
    'fd28666d72a683f5e7d3428fcf3184b9',
    'c1a3a087793ebed2cb9e59985ca1289b',
    'b44ba95d840c134949f87584797f87a5',
    '057d2dd2576282c5eab3768ac0c6031c',
    'c973624e98910af9b6d98a74c7b784a6'
]
data = []
labels = ['注册资金','单位','公司名','人数','企业类型','注册年份','行业','省市','地址','地址','区','城市','经纬','公司名称（地图）','省份','公司种类（地图）','简介']
# data['name'] =[]
f = codecs.open('output.txt', 'a+')
f.write(str(labels).encode('utf-8') + '\n')
f.close()
for counter,line in enumerate(tqdm(lines)):

    print counter//2000
    strings = re.findall(r'"([^"]*)"', line)
    data .append(  strings[3])

    fund =  [''.join(list(g)) for k, g in groupby(strings[1], key=lambda x: x.isdigit())]

    # if fund[0][0].isdigit():
    #     pass
    # else:
    #     print fund[0]
    # print '----------------------------'
    # print fund[0]
    # print fund[1]
    # print strings[3]
    # print strings[5]
    # print strings[7]
    common=''.join([item.replace('"', '') for item in line[line.index("common")+8:line.index("date")]])
    # print common
    date = ''.join([item.replace('"', '') for item in line[line.index("date")+7:line.index("productype")-3]])
    productype = ''.join([item.replace('"', '') for item in line[line.index("productype")+14:line.index("location")-3]])
    location = ''.join([item.replace('"', '') for item in line[line.index("location")+11:-1]])
    # print date
    # print productype
    # print location
    api = counter//2000
    parameter = {
        'key': api_list[api],
        'keywords': strings[3]
    }
    url = 'http://restapi.amap.com/v3/place/text?' + urlencode(parameter)
    print url
    content = urllib2.urlopen(url).read()
    parsed = json.loads(content)
    # print json.dumps(parsed, indent=4, sort_keys=True ,ensure_ascii=False).encode('utf8')
    # print str(parsed['count'])!='0'
    try:
        if str(parsed['count'])!='0':
            print parsed['count']
            print parsed['pois'][0]['address']
            print parsed['pois'][0]['adname']
            print parsed['pois'][0]['cityname']
            print parsed['pois'][0]['location']
            print parsed['pois'][0]['name']
            print parsed['pois'][0]['pname']
            print parsed['pois'][0]['type']
            # print '----------------------------'

            data = ([fund[0],fund[1],strings[3],strings[5],strings[7],date,productype,location,parsed['pois'][0]['address'],
                     parsed['pois'][0]['adname'],parsed['pois'][0]['cityname'],parsed['pois'][0]['location'],parsed['pois'][0]['name'],
                     parsed['pois'][0]['pname'],parsed['pois'][0]['type'],common])
            f = codecs.open('output.txt', 'a+')
            f.write(str(data).decode("unicode-escape")+'\n'      )
            f.close()
        else :
            data = ([fund[0], fund[1], strings[3], strings[5], strings[7], date, productype, location,common,
                         '',
                         '', '', '',
                         '',
                         '',''])
            f = codecs.open('output.txt', 'a+')
            f.write(str(data).decode("unicode-escape") + '\n')
            f.close()
    except urllib2.URLError:
        print fund[0]
        print fund[1]
        print strings[3]
        print strings[5]
        print strings[7]
        pass

    # break
    # print strings[3]
    # print line
    # line = json.loads(line)
    # # data['sfund'] = line['sfund']
    # print line['name']
    # data['name'] = line['name']

    # data['people'] = line['people']
    # data['cmptype'] = line['cmptype']
    # common = [item.replace('"', '') for item in line['common']]
    # print line['common']
    # data['common'] = pd.Series( common   )
    # data['date'] = line['date']
    # data['productype'] = line['productype']
    # data['location'] = line['location']
# data =  list(set(data))
# data = pd.DataFrame(data)
# writer = pd.ExcelWriter('output.xlsx')
# data.to_excel(writer,'Sheet1')
# company = fzzp['name']
# print company
# parameters = {
#     'keywords': company,
#
#     'key': 'e7df6d3b9eb1505c6cb758d441ee754b',
# }
#
# url= 'http://restapi.amap.com/v3/place/text?' + urlencode(parameters)
