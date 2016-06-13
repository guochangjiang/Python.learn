#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
        FILE: get.gene.detail.html.from.arabidopsis.org.by.listfile.py
       USAGE: $ python get.gene.detail.html.from.arabidopsis.org.by.listfile.py -h
 DESCRIPTION: 根据指定的拟南芥基因列表从arabidopsis.org网站获取基因的详细信息
     OPTIONS: options
REQUIREMENTS: requirements
        BUGS: bugs
      AUTHOR: guochangjiang(polaris)
     CONTACT: guochangjiang1989@gmail.com
ORGANIZATION: Nanjing University, China
     VERSION: 1.0
     CREATED: 2016/3/25 16:53:15
      UPDATE: 2016/3/25 16:53:15

 CHANGE LOGS:
     Version 1.0 2016/3/25 16:53:15    初始版本
'''

import requests

__version__ = '1.0'

url_ath = "http://www.arabidopsis.org"
search_site = "/servlets/Search?type=general&search_action=detail&method=1&show_obsolete=F&name=&sub_type=gene&SEARCH_EXACT=4&SEARCH_CONTAINS=1"

loci_list = [
            "AT1G04100.1",
            "AT1G04240.1",
            "AT1G04250.1",
            "AT1G04550.1",
            "AT1G15050.1",
            "AT1G15580.1",
            "AT1G19220.1",
            "AT1G19850.1"
]

for locus in loci_list:
    search = search_site.replace("name=", "name="+locus)
    r = requests.get(url_ath+search)
    lines = r.text.splitlines()
    for line in lines:
        if ">"+locus[:-2]+"<" in line:
            index1 = line.find('A href="')
            index2 = line.find('">'+locus[:-2]+'<')
            target_url = url_ath + line[index1+8:index2]
            print(target_url)
            target = requests.get(target_url)
            OUT = open(locus+".html", "w")
            datas = target.text.splitlines()
            for data in datas:
                try:
                    OUT.write(data+"\n")
                except:
                    pass
