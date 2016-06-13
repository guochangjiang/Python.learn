#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
        FILE: paint.gene.structure.by.requests.in.localhost.py
       USAGE: $ python paint.gene.structure.by.requests.in.localhost.py -h
 DESCRIPTION: 从http://114.212.170.95/biotools/PaintGeneStructure.v2.html中进行批量基因
              结构图绘制
     OPTIONS: options
REQUIREMENTS: requirements
        BUGS: bugs
      AUTHOR: guochangjiang(polaris)
     CONTACT: guochangjiang1989@gmail.com
ORGANIZATION: Nanjing University, China
     VERSION: 1.0
     CREATED: 2016/4/5 14:43:32
      UPDATE: 2016/4/5 14:43:32

 CHANGE LOGS:
     Version 1.0 2016/4/5 14:43:32    初始版本
'''

import argparse
import requests

__version__ = '1.0'

# 命令行参数
parser = argparse.ArgumentParser()
parser.add_argument(
                    "-i",
                    "-in",
                    "--input",
                    metavar="input_file",
                    dest="file_in",
                    required=True,
                    type=str,
                    help="file of gene structure to input")
parser.add_argument(
                    "-o",
                    "-out",
                    "--output",
                    metavar="output_file",
                    dest="file_out",
                    default="tmp.txt",
                    type=str,
                    help="file to output, [default: tmp.txt]")
parser.add_argument(
                    "-v", "--version",
                    action='version',
                    help="The version of this program.",
                    version="Version: " + __version__)
args = parser.parse_args()

with open(args.file_in) as IN:
    gene_data = IN.readlines()

url_site = "http://114.212.170.95/biotools/PaintGeneStructure.v2.html"
keyword = {
    'geneinfo': gene_data
}
r = requests.post(url_site, data=keyword)
lines = r.text.splitlines()
for line in lines:
    try:
        print(line)
    except:
        pass
