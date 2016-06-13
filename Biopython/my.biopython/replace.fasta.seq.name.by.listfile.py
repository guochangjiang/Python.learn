#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
根据指定的序列名称替换列表文件对fasta文件中的序列进行名称批量更换
"""

__version__ = '1.0'

import argparse

#命令行参数
parser = argparse.ArgumentParser()
parser.add_argument("-i",
                    "-in",
                    "--input",
                    metavar="fasta_file",
                    dest="fasta_in",
                    required=True,
                    type=str,
                    help="fasta file to process")
parser.add_argument("-o",
                    "-out",
                    "--output",
                    metavar="fasta_output",
                    dest="fasta_out",
                    default="tmp.fasta",
                    type=str,
                    help="new fasta file to output, [default: tmp.fasta]")
parser.add_argument("-nf",
                    "-name_file",
                    "--name_file",
                    metavar="name_file",
                    dest="name_file",
                    required=True,
                    type=str,
                    help="file include name list to replace")
parser.add_argument('-remain',
                    action="store_true",
                    dest="remain_flag",
                    default=False,
                    help="switch to remain the origin name")
parser.add_argument("-v",
                    "--version",
                    action='version',
                    help="The version of this program.",
                    version="Version: " + __version__)
args = parser.parse_args()

#读取替换名称列表
replace_name_dict = {}
replace_name_list = []
with open(args.name_file) as NL:
    for line in NL:
        line = line.strip()
        if line == "":
            continue
        columns = line.split()
        replace_name_list.append(columns[0])
        replace_name_dict[columns[0]] = columns[1]

#处理fasta文件
OutFasta = open(args.fasta_out, "w")
with open(args.fasta_in) as IN:
    for line in IN:
        if line[0] == ">":
            name = line.replace(">", "")
            name = name.strip()
            if name in replace_name_list:
                if args.remain_flag == True:
                    OutFasta.write(">%s|%s\n" %
                                   (name, replace_name_dict[name]))
                else:
                    OutFasta.write(">%s\n" % replace_name_dict[name])
            else:
                OutFasta.write(line)
        else:
            OutFasta.write(line)
OutFasta.close()
