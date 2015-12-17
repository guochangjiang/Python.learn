#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import re
import os
import svgwrite

#################
##子例程

#获取分支数目和总长
def GetCladeNumLength(info):
    CladeNum = 0
    AllName = []
    AllClLen = {}
    tname = re.findall("([\w\d\.\-\_\\/]+):", info) #获取所有基因名
    for name in tname:
        if re.search("[a-zA-Z\_\\/]+", name):
            AllName.append(name)
    for name in AllName:
        AllClLen[name] = GetCladeLen(name, info)
        
    return AllName, AllClLen

#获取每个基因的分支长度
def GetCladeLen(name,data):
    #print(name)
    index = data.find(name)
    fb_index = []
    rb_index = []
    index1 = 0
    while index1 < len(data) -1:
        if data[index1] != "(":
            index1 += 1
            continue
        index2 = index1 + 1
        while index2 < len(data):
            if data[index2] != ")":
                index2 += 1
                continue
            substr = data[index1:index2+1]
            if substr.count("(") == substr.count(")"):
                fb_index.append(index1)
                rb_index.append(index2)
            index2 += 1
        index1 += 1
    i = 0
    uselessinfo = []
    while i < len(fb_index):
        subinfo = data[fb_index[i]:rb_index[i]+1]
        if name not in subinfo:
            uselessinfo.append(subinfo)
        i += 1
    for nouse in uselessinfo:
        #data = re.sub(nouse+"[\d\.:]+", "", data)
        data = data.replace(nouse, "")
    n = re.search(name+":([\d\.]+)", data)
    len1 = float(n.group(1))
    p = re.findall("\)([\d\.\:]+)", data)
    len2 = 0
    for num in p:
        if ":" not in num:
            len2 += float(num)
        else:
            m = re.search("([\d\.]+):([\d\.]+)", num)
            len2 += float(m.group(2))

    return(len1,len2+len1)




#获取最小共享分支
def GetMinClade(info):
    fbindex = []
    rbindex = []
    data2return = []
    index = 0
    while index < len(info):
        if info[index] == "(":
            fbindex.append(index)
        if info[index] == ")":
            rbindex.append(index)
        index += 1
    index1 = 0
    while index1 < len(fbindex):
            index2 = 0
            while index2 < len(rbindex):
                if fbindex[index1]< rbindex[index2]:
                    data = info[fbindex[index1]+1:rbindex[index2]]
                    if ")" not in data and "(" not in data:
                        data2return.append(data)
                index2 += 1
            index1 += 1
    return data2return

################
##主程序
try:
    nwkfile = open("NB-ARC.seed.tree.nwk")
except:
    print("Cannot open file NB-ARC.seed.tree.nwk")
    os._exit(0)

nwkdata = ''
for line in nwkfile:
    line = line.strip()
    line = re.sub("\s+", "", line)
    if line == '':
        continue
    else:
        nwkdata += line
nwkfile.close()

(AllGeneName, AllCladeLen) = GetCladeNumLength(nwkdata)
MaxCladeLength = 0
#print("该系统进化树中的所有基因名、本身支长及其到根部的支长为: ")
for name in AllGeneName:
    #print(name, ":%.4f - %.4f" % (AllCladeLen[name][0], AllCladeLen[name][1]))
    if MaxCladeLength < AllCladeLen[name][1]:
        MaxCladeLength = AllCladeLen[name][1]

#print("该系统进化树的最长分支长度为: %.4f" % MaxCladeLength)
#print()
#print("-"*25)


GeneInterval = 25           #相邻分支间距
FontSize = 14               #基因名字号
MaxCladePx = 500            #最长分支画图长度
painty0 = 25                #起始y轴位置
paintx0=25                  #起始x轴位置
linecolor = "black"         #线颜色
genecolor = "black"         #基因名颜色
bootcolor = "black"         #bootstrap值颜色
nameback = 10               #基因名与线距离
strokewidth = 2             #线宽
textdown = 6                #基因名名称下移量
scalestrokewidth = 2        #比例尺线宽
scaleunit = 0.1             #比例尺大小
scalecolor = "black"        #比例尺颜色
scaletextcolor = "black"    #比例尺字体颜色

unit = MaxCladePx/MaxCladeLength

svgheight = GeneInterval * len(AllGeneName) + 100
svgweihht = MaxCladePx + 480
treepaint = svgwrite.Drawing("test.tree.svg", (svgweihht, svgheight) )
#treepaint.add(treepaint.text("test tree", insert=(20, 20), font_size = 16,fill = 'red'))

#找出每一个基因的y轴绘图位置
AllGenePy = {}
y = painty0
for gene in AllGeneName:
    AllGenePy[gene]=y
    y += GeneInterval

cladeid = 1
two = 1
flag = True
while flag:
    minclaseinfo = GetMinClade(nwkdata) #找出没有嵌套括号的括号内容
    for mininfo in minclaseinfo:
        if mininfo.count(":") > 2:
            flag = False
            last = re.findall("([a-zA-Z0-9\-/_#]+):", mininfo)
            miny = AllGenePy[last[0]]
            maxy = AllGenePy[last[0]]
            for ln in last:
                treepaint.add(treepaint.line(
                    ((AllCladeLen[ln][1]-AllCladeLen[ln][0]) * unit + paintx0, AllGenePy[ln]),
                    (AllCladeLen[ln][1] * unit + paintx0, AllGenePy[ln]),
                    stroke_width=strokewidth,
                    stroke=linecolor))
                if "#" not in ln and "merge" not in ln:
                    treepaint.add(treepaint.text(ln, insert=(AllCladeLen[ln][1] * unit + paintx0 + nameback, AllGenePy[ln]+textdown), font_size = FontSize,fill = genecolor))
                if miny > AllGenePy[ln]:
                    miny = AllGenePy[ln]
                if maxy < AllGenePy[ln]:
                    maxy = AllGenePy[ln]
            treepaint.add(treepaint.line(
                        (paintx0, miny - strokewidth / 2.0),
                        (paintx0, maxy + strokewidth / 2.0),
                        stroke_width=strokewidth,
                        stroke=linecolor))
            break
        clademergeid = "#"+str(cladeid)+"merge"
        m = re.search("^(.+):([\d\.]+),(.+):([\d\.]+)", mininfo)
        treepaint.add(treepaint.line(
                    ((AllCladeLen[m.group(1)][1]-AllCladeLen[m.group(1)][0]) * unit + paintx0, AllGenePy[m.group(1)]),
                    (AllCladeLen[m.group(1)][1] * unit + paintx0, AllGenePy[m.group(1)]),
                    stroke_width=strokewidth,
                    stroke=linecolor))
        if "#" not in m.group(1) and "merge" not in m.group(1):
            treepaint.add(treepaint.text(m.group(1), insert=(AllCladeLen[m.group(1)][1] * unit + paintx0 + nameback, AllGenePy[m.group(1)]+textdown), font_size = FontSize,fill = genecolor))
        treepaint.add(treepaint.line(
                    ((AllCladeLen[m.group(3)][1]-AllCladeLen[m.group(3)][0]) * unit + paintx0, AllGenePy[m.group(3)]),
                    (AllCladeLen[m.group(3)][1] * unit + paintx0, AllGenePy[m.group(3)]),
                    stroke_width=strokewidth,
                    stroke=linecolor))
        if "#" not in m.group(3) and "merge" not in m.group(3):
            treepaint.add(treepaint.text(m.group(3), insert=(AllCladeLen[m.group(3)][1] * unit + paintx0 + nameback, AllGenePy[m.group(3)]+textdown), font_size = FontSize,fill = genecolor))
        
        treepaint.add(treepaint.line(
                    ((AllCladeLen[m.group(1)][1]-AllCladeLen[m.group(1)][0]) * unit + paintx0, AllGenePy[m.group(1)] - strokewidth / 2.0),
                    ((AllCladeLen[m.group(3)][1]-AllCladeLen[m.group(3)][0]) * unit + paintx0, AllGenePy[m.group(3)] + strokewidth / 2.0),
                    stroke_width=strokewidth,
                    stroke=linecolor))
        n = re.search(mininfo + "\)([\d\.:]+)", nwkdata)
        mergelen = 0.0
        if ":" in n.group(1):
            b = re.search("^([\d\.]+):([\d\.]+)", n.group(1))
            boot =float(b.group(1))
            mergelen = float(b.group(2))
            boot = int(boot * 100)
            chnum = len(str(boot))
            treepaint.add(treepaint.text(str(boot), insert=((AllCladeLen[m.group(1)][1]-AllCladeLen[m.group(1)][0]) * unit + paintx0 - chnum * 8, (AllGenePy[m.group(1)] + AllGenePy[m.group(3)])/2.0 - 4), font_size = FontSize - 2, fill = bootcolor))
            nwkdata = nwkdata.replace("("+mininfo+")"+b.group(1), clademergeid)
        else:
            nwkdata = nwkdata.replace("("+mininfo+")", clademergeid)
            mergelen = float(n.group(1))
        AllCladeLen[clademergeid] = ([mergelen, AllCladeLen[m.group(1)][1]-AllCladeLen[m.group(1)][0]])
        AllGenePy[clademergeid] = (AllGenePy[m.group(1)] + AllGenePy[m.group(3)])/2.0
        cladeid += 1
    two += 1

#比例尺绘画
treepaint.add(treepaint.line(
    (paintx0 + 25, svgheight - 50),
    (paintx0 + 25 + scaleunit * unit, svgheight - 50),
    stroke_width = scalestrokewidth,
    stroke = scalecolor))
treepaint.add(treepaint.line(
    (paintx0 + 25, svgheight - 50 - scalestrokewidth * 4),
    (paintx0 + 25, svgheight - 50 + scalestrokewidth * 4),
    stroke_width = scalestrokewidth,
    stroke = scalecolor))
treepaint.add(treepaint.line(
    (paintx0 + 25 + scaleunit * unit, svgheight - 50 - scalestrokewidth * 4),
    (paintx0 + 25 + scaleunit * unit, svgheight - 50 + scalestrokewidth * 4),
    stroke_width = scalestrokewidth,
    stroke = scalecolor))
treepaint.add(treepaint.text(
    str(scaleunit),
    insert = (paintx0 + 25 + scaleunit * unit * 0.5 - len(str(scaleunit)) * 6 * 0.5, svgheight - 35),
    font_size = FontSize,
    fill = scaletextcolor))

treepaint.save()
