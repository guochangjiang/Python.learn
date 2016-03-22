#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""
从指定的vcf文件中获取其中的insert/deletion位点信息
并按样品分别输出到指定文件
"""
__version__ = '1.0'

import argparse
import re

#命令行参数处理
parser = argparse.ArgumentParser()
parser.add_argument("-i", "-in", "--input", metavar="vcf_filename", dest="input_vcf", type=str , required=True, help="vcf file to analyze")
parser.add_argument("-o", "-out", "--output", metavar="out_filename", dest="output_file", type=str, help="txt file to output, [default: inputfile.indel.info.txt]")
parser.add_argument("-v", "--version", action='version', help="The version of this program.", version = "Version: " + __version__)
args = parser.parse_args()

vcf_in = args.input_vcf #输入文件
try:
    txt_out = args.output_file
finally:
    txt_out = vcf_in.replace("vcf", "indel.info.txt")   #输出文件

position_start = -1 #vcf开始位置
position_end = -1   #vcf终止位置
indel_pos= []       #记录indel位置
ref_seq = ""        #获取参看序列
samples_list = []   #获取样本列表
indel_info_dict = {}    #记录indel位点详细信息
flank_len = 10          #从indel位点向两边扩展长度
print("Processing", "."*25, end = "")
with open(vcf_in) as IN:
    for line in IN:
        line = line.strip()
        #跳过文件头
        if line == "" or line[0:2] == '##':
            continue
        #获取样本信息并初始化indel详细信息字典
        if line[:6] == "#CHROM":
            samples_list = line.split("\t")[9:]
            for sample in samples_list:
                indel_info_dict[sample] = {}
            continue
        columns = line.split("\t")
        #获取vcf起止位置
        if position_start == -1:
            position_start = int(columns[1])
        if position_end == -1:
            position_end = int(columns[1])
        if position_start > int(columns[1]):
            position_start = int(columns[1])
        if position_end < int(columns[1]):
            position_end = int(columns[1])
        #获取位点的ref与alt碱基信息
        seq = columns[3] + "," + columns[4]
        bases = seq.split(",")
        if bases[-1] == ".":
            bases = bases[:-1]
        indel_flag = 0
        base_len = []
        #检测是否为indel位点
        for base in bases:
            base_len.append(len(base))
            if len(base) > 1:
                indel_flag = 1
        if indel_flag == 1:
            indel_pos.append(int(columns[1]))
            for index in range(9,len(columns)):
                info = columns[index]
                m = re.match("^(.)/(.)", info)
                base1 = m.group(1)
                base2 = m.group(2)
                #过滤非indel样本
                if base1 == base2 == "." or base1 == base2 == "0":
                    continue
                #处理indel样本
                # 1.按indel位置进行信息记录
                # 2.判断indel类型：ref/indel, indel/indel or indel
                # 3.记录ref序列与所有的indel相关alt序列
                base1 = int(base1)
                base2 = int(base2)
                indel_info_dict[samples_list[index-9]][columns[1]] = []
                if base1 == 0:#情况1: ref/indel杂合型
                    if base_len[base2] > base_len[0]:
                        indel_info_dict[samples_list[index-9]][columns[1]].append("ref/insertion")
                    if base_len[base2] < base_len[0]:
                        indel_info_dict[samples_list[index-9]][columns[1]].append("ref/deletion")
                    indel_info_dict[samples_list[index-9]][columns[1]].append(bases[0])
                    indel_info_dict[samples_list[index-9]][columns[1]].append(bases[base2])
                elif base1 == base2 > 0:#情况2: indel纯合型
                    btype1 = ""
                    if base_len[base1] > base_len[0]:
                        btype1 = "insertion"
                    if base_len[base1] < base_len[0]:
                        btype1 = "deletion"
                    indel_info_dict[samples_list[index-9]][columns[1]].append(btype1)
                    indel_info_dict[samples_list[index-9]][columns[1]].append(bases[0])
                    indel_info_dict[samples_list[index-9]][columns[1]].append(bases[base1])
                else:#情况3: indel杂合型
                    btype1 = ""
                    btype2 = ""
                    if base_len[base1] > base_len[0]:
                        btype1 = "insertion"
                    if base_len[base1] < base_len[0]:
                        btype1 = "deletion"
                    if base_len[base2] > base_len[0]:
                        btype2 = "insertion"
                    if base_len[base2] < base_len[0]:
                        btype2 = "deletion"
                    indel_info_dict[samples_list[index-9]][columns[1]].append(btype1 + "/" + btype2)
                    indel_info_dict[samples_list[index-9]][columns[1]].append(bases[0])
                    indel_info_dict[samples_list[index-9]][columns[1]].append(bases[base1])
                    indel_info_dict[samples_list[index-9]][columns[1]].append(bases[base2])
        #获取vcf参考序列
        else:
            ref_seq += columns[3]
print("\n")

#文件输出
TxtOut = open(txt_out, "w")
print("#Sample--position--genotype--ref--alt")
for key in samples_list:
    if indel_info_dict[key] != {}:#过滤无indel样本
        TxtOut.write("Sample:%s\n" % key)
        #按位置对indel信息进行排序
        pos_list = indel_info_dict[key].keys()
        pos_list2 = [int(pos) for pos in pos_list]
        pos_list2 = sorted(pos_list2)
        pos_list = [str(pos) for pos in pos_list2]
        #按位置对indel信息进行输出
        for pos in pos_list:
            indel_seq = "--".join(indel_info_dict[key][pos][:])
            print("%s--%s--%s" %(key, pos, indel_seq)) #屏幕简单信息输出
            #获取indel侧翼序列位置信息
            start1 = int(pos) - position_start - flank_len
            end1 = int(pos) - position_start
            ref_len = len(indel_info_dict[key][pos][1])
            start2 = int(pos) - position_start + ref_len
            end2 = int(pos) - position_start + flank_len
            ref_region = ref_seq[start1:end2] #ref片段
            alt_seq = []
            #indel序列获取
            for alt in indel_info_dict[key][pos][2:]:
                alt_seq.append(ref_seq[start1:end1] + alt + ref_seq[start2:end2])
            TxtOut.write("Position:%s\n" % pos)
            TxtOut.write("GenoType:%s\n" % indel_info_dict[key][pos][0])
            TxtOut.write("ref sequence:%s\n" % ref_region)
            for alt in alt_seq:
                TxtOut.write("alt sequence:%s\n" % alt)
        TxtOut.write("\n")