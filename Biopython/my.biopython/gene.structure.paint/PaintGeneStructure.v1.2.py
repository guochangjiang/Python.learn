#!/usr/bin/env python3
# --*-- utf-8 --*--
#
#===============================================================================
#
#		  FILE: PaintGeneStructure.v1.2.py
#
#		 USAGE: python PaintGeneStructure.v1.2.py -in geneinfo.file
#
#  DESCRIPTION: 使用svgwrite绘制基因结构图，目前仅支持两种格式
#              （gff和simple，见example）
#
#	   OPTIONS: 必须的参数只有输入文件 -in gene.info.file
# REQUIREMENTS: 需要python3以及模块svgwrite, argparse
#		  BUGS: ---
#		 NOTES: ---
#	    AUTHOR: Guo Changjiang (polaris), guochangjiang1989@gmail.com
# ORGANIZATION: Nanjing University, China
#	   VERSION: 1.2
#	   CREATED: 2015/11/09 10:58:04
#	    UPDATE: 2015/11/13 10:58:04
#===============================================================================
#   Change logs:
#   Version 1.0: 2015/11/09	初始版本，每个基因图一行，统一长度为1000px
#   Version 1.1: 2015/11/10	增加对gff文件的支持, intron折线支持, 空格分隔支持；
#                           增加自定义颜色支持，其中domain的颜色需要分别指定;
#                           增加渐变色支持；
#   Version 1.2: 2015/11/13	将比例尺统一，增加1kb长度指定

__version__ = '1.2'

import re
import os

################
##子程序
################

#将gff文件转换为simple格式，并获取内含子信息
def Gff2Simple(info):
	simpledata=[]
	AllExonDic={}
	GeneList = []
	for line in info:
		line = line.strip()
		if line == '' or re.search("^#", line):
			continue
		line = re.sub("\s+", "\t", line)
		columns = line.split("\t")
		tag = columns[2]
		tag = tag.lower()
		if tag == "domain":
			mat= re.search("domain=([a-zA-Z0-9_\-\.]+)", columns[8])
			tag2 = mat.group(1)
		if tag == "marker":
			mat= re.search("marker=([a-zA-Z0-9_\-\.]+)", columns[8])
			tag2 = mat.group(1)
		if "utr" in tag.lower():
			tag = 'utr'
		if tag not in tags:
			continue
		start = columns[3]
		end = columns[4]
		chain = columns[6]
		annotation = columns[8]
		match = re.search("^\w+=([a-zA-Z0-9_\.]+)", annotation)
		genelocus = match.group(1)
		if tag =="domain" or tag == "marker":
			simpledata.append(genelocus + "\t" + tag + "\t" + start
			                  + "\t" + end + "\t" + tag2)
		else:
			simpledata.append(genelocus + "\t" + tag + "\t" + start
			                  + "\t" + end + "\t" + chain)
		if genelocus not in GeneList:
			AllExonDic[genelocus] = ''
			GeneList.append(genelocus)

		if tag == 'exon':
			AllExonDic[genelocus] += (start + "\t" + end + "\t")
	for key in sorted(AllExonDic.keys()):
		ExonPosInfo = AllExonDic[key]
		ExonPosInfo = ExonPosInfo.strip("\t")
		AllExonNum = ExonPosInfo.split("\t")
		i = 0
		while i < len(AllExonNum):
			AllExonNum[i] = int(AllExonNum[i])
			i += 1
		AllExonNum.sort()
		i = 1
		while i + 2 < len(AllExonNum):
			simpledata.append(key + "\t" + "intron" + "\t" + str(AllExonNum[i])
			                  + "\t" + str(AllExonNum[i+1]) + "\t" + "x")
			i += 2
	return simpledata

#获取基因列表
def GetLocusList(info):
	genelist=[]
	for line in info:
		line = line.strip()
		if line == '' or re.search("^#", line):
			continue
		else:
			line = re.sub("\s+", "\t", line)
			columns = line.split("\t")
			if columns[0] not in genelist:
				genelist.append(columns[0])
	return genelist

#获取最小和最大位置
def GetMinMax(locus, info):
	MinNum = -99999
	MaxNum = -99999
	for line in info:
		line = line.strip()
		if line == '':
			continue
		line = re.sub("\s+", "\t", line)
		if locus in line:
			columns = line.split("\t")
			if columns[1] not in tags or columns[1] == "domain":
				continue
			num1 = int(columns[2])
			num2 = int(columns[3])
			if MinNum == -99999:
				MinNum = num1
			if MinNum > num1:
				MinNum = num1
			if MinNum > num2:
				MinNum = num2
			if MaxNum == -99999:
				MaxNum = num1
			if MaxNum < num1:
				MaxNum = num1
			if MaxNum < num2:
				MaxNum = num2

	return (MinNum, MaxNum)

#获取标签信息
def GetTagInfo(locus, tag, info):
	posdata=[]
	for line in info:
		line = line.strip()
		if line =='':
			continue
		line = re.sub("\s+", "\t", line)
		if locus in line:
			columns = line.split("\t")
			if tag in columns[1].lower():
				posdata.append(columns[2] + "--" + columns[3])
	return posdata

#获取链向
def GetChainOrientation(locus, info):
	posdata=[]
	for line in info:
		line = line.strip()
		if line =='':
			continue
		line = re.sub("\s+", "\t", line)
		if locus in line:
			columns = line.split("\t")
			if columns[-1] == '-' or columns[-1] == '+':
				chain = columns[-1]
				break
	return chain

#获取Domain信息
def GetDomainInfo(locus, tag, info):
	posdata=[]
	for line in info:
		line = line.strip()
		if line =='':
			continue
		line = re.sub("\s+", "\t", line)
		if locus in line:
			columns = line.split("\t")
			if tag in columns[1].lower():
				posdata.append(columns[4] + "--" + columns[2]
				               + "--" + columns[3])
	return posdata

#根据链向整理CDS信息
def SortCDSInfo(locus, tag, info):
	newinfo = []
	cdsposinfo = []
	for line in info:
		line = line.strip()
		if line == '':
			continue
		line = re.sub("\s+", "\t", line)
		if locus in line and tag in line.lower():
			newinfo.append(line)
			cdsposinfo.append(int(line.split("\t")[2]))
			cdsposinfo.append(int(line.split("\t")[3]))
	if len(newinfo) > 0:
		chain = newinfo[0].split("\t")[-1]
		if chain == "+":
			cdsposinfo.sort()
		else:
			cdsposinfo.sort(reverse=True)
	return cdsposinfo

#将domain位置转换为CDS位置
def Domain2CDS(start, length, info):
	data2return =[]
	if info[0] < info[1]:
		numinfo = GetConNum(info)
		index1 = start - 1
		index2 = index1 + length - 1
		numinfo2 = GetNumRange(numinfo[index1:index2+1])
		i = 0
		while i < len(numinfo2):
			data2return.append(str(numinfo2[i]) + "--" + str(numinfo2[i+1]))
			i += 2
		
	else:
		numinfo = GetConNum(info)
		numinfo.sort(reverse = True)
		index1 = start - 1
		index2 = index1 + length - 1
		numinfo2 = GetNumRange(numinfo[index1:index2+1])
		i = 0
		while i < len(numinfo2):
			data2return.append(str(numinfo2[i]) + "--" + str(numinfo2[i+1]))
			i += 2

	return data2return

#将位置范围转换为连续位置信息
def GetConNum(info2):
	info2.sort()
	numlist = []
	i = 1
	while i < len(info2):
		for x in range(int(info2[i-1]), int(info2[i])+1):
			numlist.append(x)
		i = i + 2
	return numlist

#将连续位置转换位置范围信息
def GetNumRange(connumlist):
	start = connumlist[0]
	rannumlist = [start,]
	i = 1
	while i < len(connumlist)-1:
		a = abs(connumlist[i]-connumlist[i-1])
		b = abs(connumlist[i]-connumlist[i+1])
		if a == 1 and b == 1:
			pass
		else:
			rannumlist.append(connumlist[i])
		i += 1
	rannumlist.append(connumlist[-1])
	return rannumlist

######################
##命令参数处理
######################
import argparse
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser(
		description = "本程序用于绘制svg格式基因结构图。输入文件信息见example。" 
		              + "\n程序版本号：v" + __version__,
		epilog = "Please Enjoy this Program!",
		formatter_class = RawTextHelpFormatter)
parser.add_argument(
		"-i", "-in", "--input",
		metavar = "genefile",
		dest = "input",
		required = True,
		type = str,
		help = "file to input")

parser.add_argument(
		"-o", "-out", "--output",
		metavar = "outfile",
		dest = "output",
		default = "output",
		type = str,
		help = "svg file to output")

parser.add_argument(
		"-f", "-format", "--format",
		metavar = "gene_info_format",
		dest = "format",
		default = "auto",
		type = str,
		help = "format of input file, e.g. auto, gff, simple. [default: auto]")

parser.add_argument(
		"-intronline", "--intronline",
		metavar = "intron_line_type",
		dest = "intronline",
		default = "straight",
		type = str,
		help = "style of intron line, e.g. straight, broken. [default: straight]")

parser.add_argument(
		"-C", "--color",
		metavar = "colors",
			dest = "colors", type=str,
		default = '',
		help = "specify colors for certain types, in the format:"
             + "\n\ttype1:color1;type2:color2;...")

parser.add_argument(
		"-kl", "--kblength",
		metavar = "length per kb",
		dest = "kblength", type=int,
		default = 250,
		help = "specify the length(px) of 1kb sequence, [default: 250]")
parser.add_argument(
		"-v", "--version",
		action = 'version',
		help = "The version of this program.",
		version = "Version: " + __version__)
args = parser.parse_args()

#######################
##颜色处理
#######################
tagcolors = {
	'cds': "green",
	'sts': "orange",
	'domain': "blue",
	'exon': "darkorange",
	'intron': "darkgrey",
	'marker': "red",
	'start_codon': "lime",
	'stop_codon': "magenta",
	'utr': "hotpink",
}

if args.colors != '':
	for pair in args.colors.split(";"):
		cpair = pair.split(":")
		tagcolors[cpair[0]] = cpair[1]

domaincolors = ["royalblue", "deeppink", "springgreen",
                "teal", "blue", "chartreuse", "yellow", "brown", "aqua"]

tags = ['utr', 'intron', 'exon', 'cds', 'sts', 'domain',
        'start_codon', 'stop_codon', 'marker']

######################
#文件格式判断
######################
fileform = ""
if args.format == "simple":
	fileform = "simple"
elif args.format == "gff":
	fileform = "gff"
elif args.format == "auto" or args.format not in dir():
	if re.search("\.gff$", args.input):
		fileform = "gff"
	else:
		fileform = 'simple'
else:
	print("ERROR file format!!!")
	os._exit(0)

######################
#文件读取
######################
infofile=open(args.input, 'r')
data = infofile.readlines()
domain_ref = "cds"
infofile.close()
if fileform == "gff":
	data = Gff2Simple(data)
locuslist = GetLocusList(data)

# 获取每个基因的长度
LocusLenDic = {}
for locus in locuslist:
	(MinPos, MaxPos) = GetMinMax(locus, data)
	LocusLenDic[locus] = MaxPos - MinPos + 1

# 获取最短基因
minlength = LocusLenDic[locuslist[0]]
minlocus = ''
for key in sorted(LocusLenDic.keys()):
	if minlength > LocusLenDic[key]:
		minlength = LocusLenDic[key]
		minlocus = key

# 获取最长基因
maxlength = LocusLenDic[locuslist[0]]
maxlocus = ''
for key in sorted(LocusLenDic.keys()):
	if maxlength < LocusLenDic[key]:
		maxlength = LocusLenDic[key]
		maxlocus = key

######################
##绘画准备
######################
import svgwrite
painty0 = 25                             #起始y轴位置
paintx0=10                               #起始x轴位置
legendx0 = 900                           #图例x轴位置
legendboxx0 = legendx0 - 5               #图例框x轴位置
piclength = 1000.0                       #基因图长度
geneinterval = 50.0                      #相邻基因间隔


kblength = args.kblength
svgout = re.sub("\.svg$", "", args.output)
gspaint = svgwrite.Drawing(svgout + ".svg", (maxlength / 1000.0 * kblength + paintx0, 320 * len(locuslist)),
                           debug = True)
# create a new linearGradient element
vertical_gradient_utr = gspaint.linearGradient((0, 0), (0, 1))
gspaint.defs.add(vertical_gradient_utr)
vertical_gradient_cds = gspaint.linearGradient((0, 0), (0, 1))
gspaint.defs.add(vertical_gradient_cds)
vertical_gradient_exon = gspaint.linearGradient((0, 0), (0, 1))
gspaint.defs.add(vertical_gradient_exon)
vertical_gradient_sts = gspaint.linearGradient((0, 0), (0, 1))
gspaint.defs.add(vertical_gradient_sts)

######################
#按照基因列表进行绘画
######################
print("\n开始绘制基因结构图：\n")
for locus in locuslist:
	print("Processing gene:" , locus, "..........")
	charnummax = 1
	#获取链向
	chain = GetChainOrientation(locus, data)
	times = 1000.0 / kblength
	legendx0 = LocusLenDic[locus] / 1000.0 * kblength - 100
	legendboxx0 = legendx0 - 5
	#显示基因名
	gspaint.add(gspaint.text(
		locus,
		insert=(paintx0, painty0),
		font_size = 16,
		fill = 'black'))
	painty0 = painty0 +60
	legendy0 = painty0 + 60
	legendboxy0 = legendy0 - 5
	unit = 1000.0
	segments = int(LocusLenDic[locus] / unit)
	halfsegments = int(LocusLenDic[locus] / 500.0)
	print("\t\t locus length:", LocusLenDic[locus])
	if halfsegments % 2 == 0:
		halfsegments = halfsegments // 2
	else:
		halfsegments = (halfsegments + 1) // 2
	#绘制链向
	if chain == '+':
		gspaint.add(gspaint.polygon(
			[(paintx0, painty0 - 25.5), (paintx0 + 40, painty0 - 25.5),
			 (paintx0 + 40, painty0 - 30.5), (paintx0 + 50, painty0 - 23),
			 (paintx0 + 40, painty0 - 15.5), (paintx0 + 40, painty0 - 20.5),
			 (paintx0, painty0 - 20.5)],
			 stroke='none', fill='gray'
		))
	else:
		gspaint.add(gspaint.polygon(
			[(paintx0 + 2 + 10, painty0 - 25), (paintx0 + 2 + 50, painty0 - 25),
			 (paintx0 + 2 + 50, painty0 - 20), (paintx0 + 2 + 10, painty0 - 20),
			 (paintx0 + 2 + 10, painty0 - 15),(paintx0 + 2, painty0 - 22.5),
			 (paintx0 + 2 + 10, painty0 - 30)],
			 stroke='none', fill='gray'
		))

	#绘制比例尺
	i = 0
	j = 1
	(MinPos, MaxPos) = GetMinMax(locus, data)
	scalex = MinPos
	while i <= segments:
		gspaint.add(gspaint.line(
			(kblength * i + paintx0, painty0-50),
			(kblength * i + paintx0, painty0-45),
			stroke_width=2,
			stroke="gray"))
		gspaint.add(gspaint.text(
			str(i) + "k",
			insert=(kblength * i + paintx0 - 6, painty0-35),
			font_size = 10,
			fill = 'black'))
		if j <= halfsegments:
			gspaint.add(gspaint.line(
				(kblength * (i + 0.5) + paintx0, painty0-50),
				(kblength * (i + 0.5) + paintx0, painty0-45),
				stroke_width=1.5,
				stroke="gray"))
			gspaint.add(gspaint.text(
				str(i) + ".5k",
				insert=(kblength * (i + 0.5) + paintx0 - 6, painty0-35),
				font_size = 10,
				fill = 'black'))
			j += 1
		
		scalex += unit
		i += 1
		scalelen = 1000.0 / LocusLenDic[locus] * piclength
		
	gspaint.add(gspaint.line(
	((MinPos - MinPos)/times + paintx0 - 1, painty0-50),
	((MaxPos - MinPos)/times + paintx0, painty0-50),
	stroke_width=3,
	stroke="black"))

	#绘制utr图例
	utrinfo = GetTagInfo(locus, 'utr', data)
	vertical_gradient_utr.add_stop_color(0, tagcolors["utr"])
	vertical_gradient_utr.add_stop_color(1, 'white')
	if len(utrinfo) > 0:
		gspaint.add(gspaint.rect(
			insert = (legendx0, legendy0+1.5),
			size = ("40px", "12px"),
			stroke_width = 0.5,
			stroke = "black",
			fill = vertical_gradient_utr.get_paint_server(default='currentColor')
		))
		gspaint.add(gspaint.text(
			"utr",
			insert = (legendx0 + 50, legendy0+12),
			font_size = 12,
			fill = 'black'))
		legendy0 += 25
		if len("utr") > charnummax:
			charnummax = len("utr")

	#绘制intron
	introninfo = GetTagInfo(locus, 'intron', data)
	for info in introninfo:
		(start, end) = info.split("--")
		start = int(start)
		end = int(end)
		if start > end:
			start, end = end, start
		length = end - start + 1
		if args.intronline == "straight":
			gspaint.add(gspaint.line(
				((start - MinPos)/times + paintx0, painty0 + 7.5),
				((end - MinPos)/times + paintx0, painty0 + 7.5),
				stroke_width = 2,
				stroke = tagcolors["intron"]))
		if args.intronline== "broken":
			gspaint.add(gspaint.line(
				((start - MinPos)/times + paintx0, painty0 + 7.5),
				((end - length / 2.0 - MinPos)/times + paintx0, painty0 + 20),
				stroke_width = 2,
				stroke = "black"))
			gspaint.add(gspaint.line(
				((end - length / 2.0 - MinPos)/times + paintx0, painty0 + 20),
				((end - MinPos)/times + paintx0, painty0 + 7.5),
				stroke_width = 2,
				stroke = "black"))
	#绘制intron图例
	if len(introninfo) > 0:
		gspaint.add(gspaint.line(
			(legendx0, legendy0+8),
			(legendx0+40, legendy0+8),
			stroke_width = 2,
			stroke = "black"))
		gspaint.add(gspaint.text(
			"intron",
			insert = (legendx0 + 50, legendy0+12),
			font_size = 12,
			fill = 'black'))
		legendy0 += 25
		if len("intron") > charnummax:
			charnummax = len("intron")

	#绘制exon
	if fileform != "gff":
		exoninfo = GetTagInfo(locus, 'exon', data)
		vertical_gradient_exon.add_stop_color(0, tagcolors["exon"])
		vertical_gradient_exon.add_stop_color(1, 'white')
		for info in exoninfo:
			(start, end) = info.split("--")
			start = int(start)
			end = int(end)
			if start < end:
				length = end - start + 1
				begin = start
			else:
				length = start - end + 1
				begin = end
			length = length / times
			gspaint.add(gspaint.rect(
				insert = ((begin - MinPos ) / times + paintx0, painty0 - 5),
				size = (str(length) + "px", "25px"),
				stroke_width = 1,
				stroke = "black",
				fill = vertical_gradient_exon.get_paint_server(default='currentColor')
			))

		#绘制exon图例
		if len(exoninfo) > 0:
			gspaint.add(gspaint.rect(
				insert = (legendx0, legendy0),
				size = ("40px", "25px"),
				stroke_width = 1,
				stroke = "black",
				fill = vertical_gradient_exon.get_paint_server(default='currentColor')
			))
			gspaint.add(gspaint.text(
				"exon",
				insert = (legendx0 + 50, legendy0+16),
				font_size = 12,
				fill = 'black'))
			legendy0 += 35
			if len("exon") > charnummax:
				charnummax = len("exon")

	#绘制utr
	vertical_gradient_utr.add_stop_color(0, tagcolors["utr"])
	vertical_gradient_utr.add_stop_color(1, 'white')
	for info in utrinfo:
		(start, end) = info.split("--")
		start = int(start)
		end = int(end)
		if start < end:
			length = end - start + 1
			begin = start
		else:
			length = start - end + 1
			begin = end
		length = length / times
		gspaint.add(gspaint.rect(
			insert = ((begin - MinPos)/times + paintx0, painty0+1.5),
			size = (str(length) + "px", "12px"),
			stroke_width = 0.5,
			stroke = "black",
			fill = vertical_gradient_utr.get_paint_server(default='currentColor')
		))

	#绘制cds
	cdsinfo = GetTagInfo(locus, 'cds', data)
	vertical_gradient_cds.add_stop_color(0, tagcolors["cds"])
	vertical_gradient_cds.add_stop_color(1, 'white')
	for info in cdsinfo:
		(start, end) = info.split("--")
		start = int(start)
		end = int(end)
		if start < end:
			length = end - start + 1
			begin = start
		else:
			length = start - end + 1
			begin = end
		length = length / times
		gspaint.add(gspaint.rect(
			insert = ((begin - MinPos) / times + paintx0, painty0 - 5),
			size = (str(length) + "px", "25px"),
			stroke_width = 1,
			stroke = "black",
			fill = vertical_gradient_cds.get_paint_server(default='currentColor'),
			opacity = 1.0  #不透明度（待添加功能）
			))

	#绘制cds图例
	if len(cdsinfo) > 0:
		gspaint.add(gspaint.rect(
			insert = (legendx0, legendy0),
			size = ("40px", "25px"),
			stroke_width = 1,
			stroke = "black",
			fill = vertical_gradient_cds.get_paint_server(default='currentColor')
		))
		gspaint.add(gspaint.text(
			"CDS",
			insert = (legendx0 + 50, legendy0+16),
			font_size = 12,
			fill = 'black'))
		legendy0 += 35
		if len("CDS") > charnummax:
			charnummax = len("CDS")

	#绘制sts
	stsinfo = GetTagInfo(locus, 'sts', data)
	vertical_gradient_sts.add_stop_color(0, tagcolors["sts"])
	vertical_gradient_sts.add_stop_color(1, 'white')
	for info in stsinfo:
		(start, end) = info.split("--")
		start = int(start)
		end = int(end)
		if start < end:
			length = end - start + 1
			begin = start
		else:
			length = start - end + 1
			begin = end
		length = length / times
		gspaint.add(gspaint.rect(
			insert = ((begin - MinPos) / times + paintx0, painty0 - 5),
			size = (str(length) + "px", "25px"),
			stroke_width = 1,
			stroke = "black",
			fill = vertical_gradient_sts.get_paint_server(default='currentColor')
		))

	#绘制sts图例
	if len(stsinfo) > 0:
		vertical_gradient.add_stop_color(0, tagcolors["sts"])
		vertical_gradient.add_stop_color(1, 'white')
		gspaint.add(gspaint.rect(
			insert = (legendx0, legendy0),
			size = ("40px", "25px"),
			stroke_width = 1,
			stroke = "black",
			fill = vertical_gradient.get_paint_server(default='currentColor')
		))
		gspaint.add(gspaint.text(
			"CDS",
			insert = (legendx0 + 50, legendy0+16),
			font_size = 12,
			fill = 'black'))
		legendy0 += 35
		if len("sts") > charnummax:
			charnummax = len("sts")

	#绘制domain
	cdsposdata = SortCDSInfo(locus, domain_ref, data)
	if cdsposdata ==[]:
		cdsposdata = SortCDSInfo(locus, "exon", data)  #以CDS为domain位置判断首选

	domaininfo = GetDomainInfo(locus, 'domain', data)
	domainlist = []
	for line in domaininfo:
		domainlist.append(line.split("--")[0])

	domainset= list(set(domainlist))
	domainset.sort()
	domainsetcolors={}
	index = 0
	indexcolor = 0
	while index < len(domainset):
		if domainset[index] in tagcolors.keys():
			domainsetcolors[domainset[index]] = tagcolors[domainset[index]]
		else:
			domainsetcolors[domainset[index]] = domaincolors[index]
			i += 1
		index += 1

	for line in domaininfo:
		(domain, aa1, aa2) = line.split("--")
		aa1 = int(aa1)
		aa2 = int(aa2)
		nucl0 = aa1 * 3 - 2
		length = (aa2 - aa1 + 1) * 3
		domain2cdsinfo = Domain2CDS(nucl0, length, cdsposdata)
		domainsave=[];
		vertical_gradient_domain = gspaint.linearGradient((0, 0), (0, 1))
		gspaint.defs.add(vertical_gradient_domain)
		vertical_gradient_domain.add_stop_color(0, domainsetcolors[domain])
		vertical_gradient_domain.add_stop_color(1, 'white')
		for info in domain2cdsinfo:
			(start, end) = info.split("--")
			start = int(start)
			end = int(end)
			if start < end:
				length = end - start + 1
				begin = start
			else:
				length = start - end + 1
				begin = end
			length = length / times
			gspaint.add(gspaint.rect(
				insert = ((begin - MinPos) / times + paintx0, painty0 - 5),
				size = (str(length) + "px", "25px"),
				stroke_width = 1,
				stroke = "black",
				fill = vertical_gradient_domain.get_paint_server(default='currentColor')
			))
			#绘制domain图例
			if domain not in domainsave:
				gspaint.add(gspaint.rect(
					insert = (legendx0, legendy0),
					size = ("40px", "25px"),
					stroke_width = 1,
					stroke = "black",
					fill = vertical_gradient_domain.get_paint_server(default='currentColor')
				))
				gspaint.add(gspaint.text(
					domain,
					insert = (legendx0 + 50, legendy0+16.5),
					font_size = 12,
					fill = 'black'))
				legendy0 += 35
				domainsave.append(domain)
				if len(domain) > charnummax:
					charnummax = len(domain)

	#绘制图例框
	legendy0 -= 5
	lines = gspaint.add(gspaint.g(stroke_width=2, stroke='gray', fill='none'))
	endlegendx = legendboxx0 + 65 + charnummax * 7
	lines.add(gspaint.polyline(
		[(legendboxx0, legendboxy0), (endlegendx, legendboxy0),
		 (endlegendx, legendy0), (legendboxx0, legendy0),
		 (legendboxx0, legendboxy0)]))


	#绘制start codon
	stcodoninfo = GetTagInfo(locus, 'start_codon', data)
	for info in stcodoninfo:
		(start, end) = info.split("--")
		start = int(start)
		end = int(end)
		if start < end:
			length = end - start + 1
			begin = start
		else:
			length = start - end + 1
			begin = end
		length = length / times
		if length < 2:
			length = 2
		gspaint.add(gspaint.rect(
			insert = ((begin - MinPos) / times + paintx0, painty0 - 12.5),
			size = (str(length) + "px", "40px"),
			stroke_width = 1,
			stroke = tagcolors["start_codon"],
			fill = tagcolors["start_codon"]))
		gspaint.add(gspaint.text(
			"ATG",
			insert = ((begin - MinPos) / times + paintx0 - 10, painty0 + 42),
			font_size = 10,
			fill = 'black'))

	#绘制stop codon
	endcodoninfo = GetTagInfo(locus, 'stop_codon', data)
	for info in endcodoninfo:
		(start, end) = info.split("--")
		start = int(start)
		end = int(end)
		if start < end:
			length = end - start + 1
			begin = start
		else:
			length = start - end + 1
			begin = end
		length = length / times
		if length < 2:
			length = 2
		gspaint.add(gspaint.rect(
			insert = ((begin - MinPos)/times - 2 + paintx0, painty0 - 12.5),
			size = (str(length) + "px", "40px"),
			stroke_width = 1,
			stroke = tagcolors["stop_codon"],
			fill = tagcolors["stop_codon"]))
		gspaint.add(gspaint.text(
			"TAG",
			insert = ((begin - MinPos) / times - 10 + paintx0, painty0 + 42),
			font_size = 10,
			fill = 'black'))

	#绘制marker
	markerinfo = GetDomainInfo(locus, 'marker', data)
	for info in markerinfo:
		(marker, start, end) = info.split("--")
		start = int(start)
		end = int(end)
		if start < end:
			length = end - start + 1
			begin = start
		else:
			length = start - end + 1
			begin = end
		length = length / times
		if length < 2:
			length = 2
		gspaint.add(gspaint.rect(
			insert = ((begin - MinPos)/times - 2 + paintx0, painty0 - 12.5),
			size = (str(length) + "px", "40px"),
			stroke_width = 1,
			stroke = tagcolors["marker"],
			fill = tagcolors["marker"]))
		marker2 = marker.strip('\"')
		charnum = len(marker2) + 0.5
		gspaint.add(gspaint.text(
			marker2,
			insert = ((begin - MinPos) / times + paintx0
			           + (length - 7 * charnum) / 2, painty0 -20),
			font_size = 10,
			fill = 'red'))

	painty0 = legendy0 + geneinterval   #下个基因绘制y轴位置

######################
##保存图像
gspaint.save()

print()
print("-------------------------")
print("The outfile:\n" + svgout + ".svg")
print("""
-------------------------
Success!!!
Congratulations to you!!!
-------------------------"""
)