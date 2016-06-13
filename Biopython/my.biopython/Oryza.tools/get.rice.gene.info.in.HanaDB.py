#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
        FILE: get.rice.gene.info.in.HanaDB.py
       USAGE: $ python get.rice.gene.info.in.HanaDB.py -h
 DESCRIPTION: 在网站Hana-DB OS(http://evolver.psc.riken.jp/seiken/OS/search.html)中查询指定水稻基因(RAP&MSU ID)列表中
              基因的表达水平详情图输出到指定目录
     OPTIONS: -nf name_file -dir out_dir
REQUIREMENTS: RAP or MSU locus id, i.e. OS01Gxxxx
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

url_site = 'http://evolver.psc.riken.jp/seiken/OS/search.cgi'
for locus in loci_list:
    print('Searching %s in Hana-DB OS .....' % locus)
    if '.' in locus:
        locus = re.sub('\.\d+$', '', locus)
    keyword = {'id': locus}
    r = requests.post(url_site, data=keyword)
    print(r.text)
'''
    no_hit = 'unknown gene'
    if no_hit in r.text:
        print("\t%s Not Found!" % locus)
        continue
    datas = r.text.splitlines()
    for data in datas:
        try:
            if 'please see this image only' in data:
                m = re.search('href="(.+)"', data)
                image_name = m.group(1)
                image_name = image_name.replace(r"../tmp/","")
                print("Download Image File=", image_name)
                r = requests.get('http://evolver.psc.riken.jp/seiken/tmp/'+image_name, stream=True)
                with open(args.dir_out+"/"+locus+".png", 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk: # filter out keep-alive new chunks
                            f.write(chunk)
                            f.flush()
                f.close()
        except:
            print("\tError in processing", locus)
'''