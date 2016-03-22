#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""
从指定的vcf文件中获取其中的insert/deletion位点信息并提取到新的vcf文件中
"""
__version__ = '1.0'

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "-in", "--input", metavar="vcf_filename", dest="input_vcf", type=str , required=True, help="vcf file to analyze")
parser.add_argument("-o", "-out", "--output", metavar="vcf_filename", dest="output_vcf", type=str, help="vcf file to analyze, [default: inputfile.indel.vcf]")
parser.add_argument("-v", "--version", action='version', help="The version of this program.", version = "Version: " + __version__)
args = parser.parse_args()
print(args)

vcf_in = args.input_vcf
print(vcf_in)
try:
    vcf_out = args.output_vcf
finally:
    vcf_out = vcf_in.replace("vcf", "indel.vcf")
print(vcf_out)

position_last = 0 #上一位置信息
indel_count = 0   #indel计数

OutVcf = open(vcf_out, "w")
with open(vcf_in) as IN:
    for line in IN:
        print(position_last)
        if line[0] == "#":
            OutVcf.write(line)
            continue
        columns = line.split("\t")
        if len(columns) < 8:
            continue
        if position_last == 0:
            position_last = int(columns[1])
            continue
        else:
            if position_last == int(columns[1]) or len(columns[3]) > 1:
                OutVcf.write(line)
                indel_count += 1
                position_last = int(columns[1])
            else:
                position_last = int(columns[1])

OutVcf.close()
print("The number of indel sites: %d" % indel_count)