#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#
#===============================================================================
#
#         FILE: Paint.Gene.In.Chr.v1.0.py
#
#        USAGE: usage
#
#  DESCRIPTION:
#
#      OPTIONS: ---
# REQUIREMENTS:
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: Guo Changjiang (polaris), guochangjiang1989@gmail.com
# ORGANIZATION: Nanjing University, China
#      VERSION: 1.0
#      CREATED: 2015/12/23 16:48:19
#       UPDATE: 2015/12/23 16:48:19
#===============================================================================
#   Change logs:
#   Version

__version__ = '1.0'

import re

#######
##子例程

##染色体信息获取
def GetChrInfo(info):
    chrinfo = {}
    for line in info:
        columns = line.split()
        if columns[0] == "chromosome" or "chr" in columns[0]:
            chrnum = columns[1]
            chrnum = chrnum.lower()
            chrnum = re.sub("chr", "", chrnum)
            chrnum = str(int(chrnum))
            chrinfo[chrnum] = [int(columns[2]), int(columns[3])]
    return chrinfo

##着丝粒信息获取
def GetCenInfo(info):
    ceninfo = {}
    for line in info:
        columns = line.split()
        if columns[0] == "centromere":
            chrnum = columns[1]
            chrnum = chrnum.lower()
            chrnum = re.sub("chr", "", chrnum)
            chrnum = str(int(chrnum))
            ceninfo[chrnum] = [int(columns[2]), int(columns[3])]
    return ceninfo

##########
##主程序

InFile = open("geneposinfo.txt", "r")
data = []
for line in InFile:
    line = line.strip()
    if line == '' or re.search("^#", line):
        continue
    data.append(line)
InFile.close()

##获取染色体信息
ChrData = GetChrInfo(data)
##获取着丝粒信息
CenData = GetCenInfo(data)
##获取最长染色体长度
maxlen = 0
for key in sorted(ChrData.keys()):
    length = ChrData[key][1]-ChrData[key][0]+1
    if maxlen < length:
        maxlen = length


##绘图
import svgwrite
paintx0 = 25    #绘图起始位置
painty0 = 25    #绘图起始位置
maxlength = 500.0 #最长染色体绘图长度
chrintervals = 150    #染色体间距
cencolor = "gray" #着丝粒颜色
genecirR = "5"
genecolor = "red"

unit = maxlength / maxlen #每bp绘图长度
gppaint = svgwrite.Drawing("yang.genepos.svg", (len(ChrData.keys()) * chrintervals - chrintervals + 200, maxlength + 50), debug = True)

##染色体绘制
ChrPaintX = {}
for key in sorted(ChrData.keys()):
    chr = int(key)
    chrx = chr * chrintervals - chrintervals + 25
    ChrPaintX[key] = chrx
    length = ChrData[key][1] - ChrData[key][0] + 1
    gppaint.add(gppaint.text(
        "chr"+key,
        insert = (chrx-15, painty0),
        font_size = 16,
        fill = "black"))
    gppaint.add(gppaint.line(
        (chrx, painty0+5),
        (chrx, painty0 + 5 + (length * maxlength / maxlen)),
        stroke_width = 3,
        stroke = "black"))
    ##着丝粒绘制
    try:
        gppaint.add(gppaint.line(
            (chrx, painty0 + 5 + CenData[key][0] * unit - unit),
            (chrx, painty0 + 5 + CenData[key][1] * unit - unit),
            stroke_width = 6,
            stroke = cencolor))
    except:
        pass

##基因绘制
for line in data:
    columns = line.split()
    if columns[0] == "chromosome" or columns[0] == "centromere":
        continue
    gene = columns[0]
    chrnum = columns[1]
    chrnum = chrnum.lower()
    chrnum = re.sub("chr", "", chrnum)
    chrnum = str(int(chrnum))
    genepos = (int(columns[3]) + int(columns[2])) * 0.5
    #print(gene, columns[2], columns[3], genepos)
    gppaint.add(gppaint.circle(
        center = (ChrPaintX[chrnum], painty0 + 5 + genepos * unit - unit),
        r = genecirR+"px",
        fill = genecolor))
    gppaint.add(gppaint.text(
        gene,
        insert = (ChrPaintX[chrnum] + 10, painty0 + 10 + genepos * unit - unit),
        font_size = 14,
        fill = "black"))

gppaint.save()
