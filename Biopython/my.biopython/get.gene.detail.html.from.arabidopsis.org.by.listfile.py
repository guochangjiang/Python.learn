#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
        FILE: get.gene.detail.html.from.arabidopsis.org.by.listfile.py
       USAGE: $ python get.gene.detail.html.from.arabidopsis.org.by.listfile.py -h
 DESCRIPTION: 根据指定的拟南芥基因列表从arabidopsis.org网站获取基因的详细信息，
              并获取的网页保存到指定目录
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
import argparse
import os
import re

__version__ = '1.0'

# 命令行参数
parser = argparse.ArgumentParser()
parser.add_argument(
                    "-nf",
                    "-namefile",
                    "--namefile",
                    metavar="name_file",
                    dest="name_file",
                    required=True,
                    type=str,
                    help="file of gene list to search")
parser.add_argument(
                    "-d",
                    "-dir",
                    "--dir",
                    metavar="output_dir",
                    dest="dir_out",
                    default=".",
                    type=str,
                    help="directory to output, [default: 当前目录]")
parser.add_argument(
                    "-v", "--version",
                    action='version',
                    help="The version of this program.",
                    version="Version: " + __version__)
args = parser.parse_args()


url_ath = "http://www.arabidopsis.org"
search_site = "/servlets/Search?type=general&search_action=detail&method=1&show_obsolete=F&name=&sub_type=gene&SEARCH_EXACT=4&SEARCH_CONTAINS=1"

# get gene list
loci_list = []
with open(args.name_file) as IN:
    for line in IN:
        line = line.strip()
        if line == "":
            continue
        if line not in loci_list:
            loci_list.append(line)
# out dir
if args.dir_out != "." and not os.path.exists(args.dir_out):
    os.makedirs(args.dir_out)

for locus in loci_list:
    print("Searching %s in arabidopsis.org ...." % locus)
    if "." in locus:
        locus = re.sub("\.\d+$", "", locus)
    search = search_site.replace("name=", "name="+locus)
    # print(url_ath + search)
    r = requests.get(url_ath + search)
    lines = r.text.splitlines()
    locus_flag = 0
    name_flag = 0
    describ = 0
    for line in lines:
        if ">"+locus+"</A>" in line:
            # print(locus, line)
            locus_flag = 1
            index1 = line.find('A href="')
            index2 = line.find('">'+locus+'<')
            target_url = url_ath + line[index1+8:index2]
            # print(target_url)
            target = requests.get(target_url)
            OUT = open(args.dir_out + "/" + locus+".html", "w")
            datas = target.text.splitlines()
            body_flag = 0
            table_flag = 0
            for data in datas:
                try:
                    if '<body>' in data:
                        body_flag = 1
                    if '<table' in data:
                        table_flag = 1
                    if body_flag == 1 and table_flag == 0:
                        pass
                    elif re.search("[^\s+]", data):
                        OUT.write(data+"\n")
                except:
                    pass
                if '>Description' in data:
                    describ = 1
                    continue
                if '>Other names:' in data:
                    name_flag = 1
                    continue
                if 1 <= describ < 3:
                    describ += 1
                    if describ == 3:
                        data = re.sub("^\s+", "", data)
                        data = data.replace('<td class="sm" >', '')
                        data = data.replace('</td>', '')
                        print("\tDescription:%s" % data)
                if 1 <= name_flag < 6:
                    name_flag += 1
                    if name_flag == 6:
                        data = re.sub('^\s+<td class="sm">', '', data)
                        data = data.replace('</td>', '')
                        print('\tOther name:%s' % data)
    if locus_flag == 0:
        print("\t%s Not Found!" % locus)
