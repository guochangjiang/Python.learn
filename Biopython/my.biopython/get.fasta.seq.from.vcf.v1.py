#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""
从指定的vcf文件(某一段序列，如一个基因)生成fasta格式文件信息：
    1. 把杂合位点转变为简并碱基
    2. 支持样品信息添加
    3. 忽略indel信息
    4. 不支持reference文件
    5. 不支持指定染色体与位置
"""

__version__ = '1.0'

#简并碱基转换
def DegenerateBasePair(basepair):
    basepair = basepair.upper()
    l = list(basepair)
    l.sort()
    basepair = "".join(l)
    if basepair == "A":
        return "A"
    elif basepair == "G":
        return "G"
    elif basepair == "T":
        return "T"
    elif basepair == "C":
        return "C"
    elif basepair == "AC":
        return "M"
    elif basepair == "AG":
        return "R"
    elif basepair == "AT":
        return "W"
    elif basepair == "CG":
        return "S"
    elif basepair == "CT":
        return "Y"
    elif basepair == "GT":
        return "K"
    elif basepair == "ACG":
        return "V"
    elif basepair == "ACT":
        return "H"
    elif basepair == "AGT":
        return "D"
    elif basepair == "CGT":
        return "B"
    else:
        return "N"


import argparse
import os
import re

#命令行参数
parser = argparse.ArgumentParser()
parser.add_argument("-i", "-in", "--input", metavar="vcf_filename", dest="input_vcf", type=str , required=True, help="vcf file to analyze")
#parser.add_argument("-o", "-out", "--output", metavar="fasta_filename", dest="output_fasta", type=str, help="fasta file to output, [default: prefix.sample.fasta]")
parser.add_argument("-pre", "--prefix", metavar="prefix_outfasta", dest="prefix_fasta", default="undefined", type=str, help="prefix of fasta file to output, [default: undefined]")
parser.add_argument("-name", "--name", metavar="name_prefix", dest="name_prefix", default="gene", type=str, help="prefix of sequence name, [default: gene]")
parser.add_argument("-d", "-dir", "--dir", metavar="dir_output", dest="dir_fasta", default="VcfFasta", type=str, help="directory of fasta file to output, [default: VcfFasta]")
parser.add_argument("-si", "-sampleinfo", "--sample_infomation", metavar="sample_info", dest="sample_info", default="None", type=str, help="information of sample to add sequence name [default: none]")
parser.add_argument("-v", "--version", action='version', help="The version of this program.", version = "Version: " + __version__)
args = parser.parse_args()

#输出目录
if not os.path.exists(args.dir_fasta):
    os.makedirs(args.dir_fasta)
    
#样品信息
samples_dict = {}
if args.sample_info != "None":
    with open(args.sample_info) as SI:
        for line in SI:
            line = line.strip()
            if line == "":
                continue
            columns = line.split()
            samples_dict[columns[0]] = "|".join(columns[1:])

samples_list = []
fasta_dict = {}

with open(args.input_vcf) as VCF:
    for line in VCF:
        line = line.strip()
        if line == "" or line[0:2] == '##':
            continue
        if line[:6] == "#CHROM":
            samples_list = line.split("\t")[9:]
            for sample in samples_list:
                fasta_dict[sample] = ""
            continue
        columns = line.split("\t")
        seq = columns[3] + "," + columns[4]
        bases = seq.split(",")
        if bases[-1] == ".":
            bases = bases[:-1]
        indel_flag = 0
        for base in bases:
            if len(base) > 1:
                indel_flag = 1
                break
        if indel_flag == 1:
            continue
        for index in range(9,len(columns)):
            info = columns[index]
            m = re.match("^(.)/(.)", info)
            base1 = m.group(1)
            base2 = m.group(2)
            if base1 == "." and base2 == ".":
                fasta_dict[samples_list[index-9]] += "N"
            else:
                base1 = int(base1)
                base2 = int(base2)
                if base1 == base2:
                    fasta_dict[samples_list[index-9]] += bases[base1]
                else:
                    fasta_dict[samples_list[index-9]] += DegenerateBasePair(bases[base1]+bases[base2])

#输出到总文件与分样品文件
TotalOut = open(args.dir_fasta + "/" + args.prefix_fasta + ".fasta", "w")
for sample in samples_list:
    OutFasta = open(args.dir_fasta + "/" + args.prefix_fasta + "." + sample + ".fasta", "w")
    OutFasta.write(">%s|%s" % (args.name_prefix, sample))
    TotalOut.write(">%s|%s" % (args.name_prefix, sample))
    if sample in samples_dict.keys():
        OutFasta.write("|%s" % samples_dict[sample])
        TotalOut.write("|%s" % samples_dict[sample])
    OutFasta.write("\n%s\n" % fasta_dict[sample])
    TotalOut.write("\n%s\n" % fasta_dict[sample])
    OutFasta.close()
TotalOut.close()