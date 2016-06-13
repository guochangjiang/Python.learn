#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
        FILE: get.rice.gene.detail.from.RAP_DB.by.listfile.py
       USAGE: $ python get.rice.gene.detail.from.RAP_DB.by.listfile.py -h
 DESCRIPTION: 在网站RAP-DB(http://rapdb.dna.affrc.go.jp)中查询指定水稻基因(RAP ID)列表中
              已报道基因的详细信息并以原始网页形式输出到指定文件夹
     OPTIONS: -nf name_file -dir out_dir
REQUIREMENTS: RAP locus id, i.e. OS01Gxxxx
        BUGS: bugs
      AUTHOR: guochangjiang(polaris)
     CONTACT: guochangjiang1989@gmail.com
ORGANIZATION: Nanjing University, China
     VERSION: 1.0
     CREATED: 2016/3/28 16:36:05
      UPDATE: 2016/3/28 16:36:05

 CHANGE LOGS:
     Version 1.0 2016/3/28 16:36:05    初始版本
'''

import argparse
import re
import os
import requests

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
                    help="file of gene list")
parser.add_argument(
                    "-d",
                    "-dir",
                    "--dir",
                    metavar="output_dir",
                    dest="dir_out",
                    default=".",
                    type=str,
                    help="dir to output, [default: 当前目录]")
parser.add_argument(
                    "-v", "--version",
                    action='version',
                    help="The version of this program.",
                    version="Version: " + __version__)
args = parser.parse_args()

# get gene list
loci_list = []
with open(args.name_file) as IN:
    for line in IN:
        line = line.strip()
        if line == '':
            continue
        loci_list.append(line)

# out dir
if args.dir_out != "." and not os.path.exists(args.dir_out):
    os.makedirs(args.dir_out)

url_site = 'http://rapdb.dna.affrc.go.jp/tools/search/run?keyword=&id=on&attr=desc&attr=cgs&attr=cgn&attr=cgss&attr=cgns'
for locus in loci_list:
    print('Searching %s in RAP-DB .....' % locus)
    if '.' in locus:
        locus = re.sub('\.\d+$', '', locus)
    search_site = url_site.replace('keyword=', 'keyword='+locus)
    r = requests.get(search_site)
    no_hit = 'There were no genes that matched your query'
    if no_hit in r.text:
        print("\t%s Not Found!" % locus)
        continue
    datas_1 = r.text.splitlines()
    OUT_1 = open(args.dir_out + '/' + locus + '.simple.html', 'w')
    detail_url = ''
    body_flag = 0
    content_flag = 0
    for data in datas_1:
        try:
            if '<body>' in data:
                body_flag = 1
            if 'id="content"' in data:
                content_flag = 1
            if body_flag == 1 and content_flag == 0:
                pass
            elif re.search('[^\s+]', data):
                OUT_1.write(data + '\n')
            if '>' + locus +'<' in data:
                m = re.search('<a href="(.+)" target', data)
                detail_url = m.group(1)
        except:
            pass
    OUT_1.close()
    r = requests.get('http://rapdb.dna.affrc.go.jp'+detail_url)
    print('http://rapdb.dna.affrc.go.jp'+detail_url)
    datas_2 = r.text.splitlines()
    OUT_2 = open(args.dir_out + '/' + locus + '.detail.html', 'w')
    body_flag = 0
    content_flag = 0
    for data in datas_2:
        try:
            if '<body>' in data:
                body_flag = 1
            if 'id="content"' in data or "id='content'" in data:
                content_flag = 1
            if body_flag == 1 and content_flag == 0:
                pass
            elif re.search('[^\s+]', data):
                OUT_2.write(data + '\n')
        except:
            pass
    OUT_2.close()
