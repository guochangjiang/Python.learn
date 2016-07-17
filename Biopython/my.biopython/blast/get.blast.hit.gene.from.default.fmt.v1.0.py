#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
        FILE: get.blast.hit.gene.from.default.fmt.v1.0.py
       USAGE: $ python get.blast.hit.gene.from.default.fmt.v1.0.py -h
 DESCRIPTION: get gene name list from blast+ results content
     OPTIONS: -in blast.results.txt -out gene.list.csv
REQUIREMENTS: text file of blast+ result(default format out)
        BUGS: bugs
      AUTHOR: guochangjiang(polaris)
     CONTACT: guochangjiang1989@gmail.com
ORGANIZATION: Nanjing University, China
     VERSION: 1.0
     CREATED: 2016/7/1 9:52:18
      UPDATE: 2016/7/1 9:52:18

 CHANGE LOGS:
     Version 1.0 2016/7/1 9:52:18    初始版本: 从blast+默认输出结果中获取基因名列表
'''

import argparse

__version__ = '1.0'

# 命令行参数
parser = argparse.ArgumentParser()
parser.add_argument(
                    "-i",
                    "-in",
                    "--input",
                    metavar="input_file",
                    dest="fasta_in",
                    required=True,
                    type=str,
                    help="file to input")
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

