#!/usr/bin/env python3
# --*-- utf-8 --*--
#
#===============================================================================
#
#		 FILE: PaintGeneStructure.py
#
#		USAGE: usage
#
#  DESCRIPTION: 使用svgwrite绘制基因结构图
#
#	  OPTIONS: ---
# REQUIREMENTS: 需要python3以及模块svgwrite, argparse
#		 BUGS: ---
#		NOTES: ---
#	   AUTHOR: Guo Changjiang (polaris), guochangjiang1989@gmail.com
# ORGANIZATION: Nanjing University, China
#	  VERSION: 1.1
#	  CREATED: 2015/11/09 10:58:04
#	   UPDATE: 2015/11/10 10:58:04
#===============================================================================
#   Change logs:
#   Version 1.0: 2015/11/09	初始版本
#   Version 1.1: 2015/11/10	增加对gff文件的支持


__version__ = '1.0'

import re
import os

##子程序
def Gff2Simple(info):
	simpledata=[]
	AllExonDic={}
	GeneList = []
	for line in info:
		line = line.strip()
		if line == '' or re.search("^#", line):
			continue
		columns = line.split("\t")
		tag = columns[2]
		if "utr" in tag.lower():
			tag = 'utr'
		if tag.lower() not in tags:
			continue
		start = columns[3]
		end = columns[4]
		chain = columns[6]
		annotation = columns[8]
		match = re.search("^\w+=([a-zA-Z0-9_\.]+)", annotation)
		genelocus = match.group(1)
		#print(genelocus)
		simpledata.append(genelocus + "\t" + tag + "\t" + start + "\t" + end + "\t" + chain)
		if genelocus not in GeneList:
			AllExonDic[genelocus] = ''
			GeneList.append(genelocus)
		if tag == 'exon':
			AllExonDic[genelocus] += (start + "\t" + end + "\t")
	for key in sorted(AllExonDic.keys()):
		#print(AllExonDic[key])
		ExonPosInfo = AllExonDic[key]
		ExonPosInfo = ExonPosInfo.strip("\t")
		AllExonNum = ExonPosInfo.split("\t")
		AllExonNum.sort()
		i = 1
		while i + 2 < len(AllExonNum):
			simpledata.append(key + "\t" + "intron" + "\t" + AllExonNum[i] + "\t" + AllExonNum[i+1] + "\t" + "x")
			i += 2
	return simpledata


def GetLocusList(info):
	genelist=[]
	for line in info:
		line = line.strip()
		if line == '' or re.search("^#", line):
			continue
		else:
			columns = line.split("\t")
			if columns[0] not in genelist:
				genelist.append(columns[0])
	return genelist

def GetMinMax(locus, info):
	MinNum = -99999
	MaxNum = -99999
	for line in info:
		line = line.strip()
		if line == '':
			continue
		if locus in line:
			columns = line.split("\t")
			if columns[1] not in tags:
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

def GetTagInfo(locus, tag, info):
	posdata=[]
	for line in info:
		line = line.strip()
		if line =='':
			continue
		if locus in line:
			columns = line.split("\t")
			if tag in columns[1].lower():
				posdata.append(columns[2] + "-" + columns[3])
	return posdata

def GetChainOrientation(locus, info):
	posdata=[]
	for line in info:
		line = line.strip()
		if line =='':
			continue
		if locus in line:
			columns = line.split("\t")
			chain = columns[-1]
			break
	return chain

def GetDomainInfo(locus, tag, info):
	posdata=[]
	for line in info:
		line = line.strip()
		if line =='':
			continue
		if locus in line:
			columns = line.split("\t")
			if tag in columns[1].lower():
				posdata.append(columns[4] + "-" + columns[2] + "-" + columns[3])
	return posdata

def SortCDSInfo(locus, tag, info):
	newinfo = []
	cdsposinfo = []
	for line in info:
		line = line.strip()
		if line == '':
			continue
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

def Domain2CDS(start, length, info):
	data2return =[]
	if info[0] < info[1]:
		numinfo = GetConNum(info)
		index1 = start - 1
		index2 = index1 + length - 1
		numinfo2 = GetNumRange(numinfo[index1:index2+1])
		i = 0
		while i < len(numinfo2):
			data2return.append(str(numinfo2[i]) + "-" + str(numinfo2[i+1]))
			i += 2
		
	else:
		numinfo = GetConNum(info)
		numinfo.sort(reverse = True)
		index1 = start - 1
		index2 = index1 + length - 1
		numinfo2 = GetNumRange(numinfo[index1:index2+1])
		i = 0
		while i < len(numinfo2):
			data2return.append(str(numinfo2[i]) + "-" + str(numinfo2[i+1]))
			i += 2

	return data2return

def GetConNum(info2):
	info2.sort()
	numlist = []
	i = 1
	while i < len(info2):
		for x in range(int(info2[i-1]), int(info2[i])+1):
			numlist.append(x)
		i = i + 2
	return numlist

def GetNumRange(connumlist):
	start = connumlist[0]
	rannumlist = [start,]
	i = 1
	while i < len(connumlist)-1:
		if abs(connumlist[i]-connumlist[i-1]) == 1 and abs(connumlist[i]-connumlist[i+1]) == 1:
			pass
		else:
			rannumlist.append(connumlist[i])
		i += 1
	rannumlist.append(connumlist[-1])
	return rannumlist



##参数处理
import argparse
parser = argparse.ArgumentParser(
		description="Version: " + __version__,
		epilog="Please Enjoy this Program!")
parser.add_argument(
		"-i", "-in", "--input",
		metavar="genefile",
		dest="input",
		type=str,
		help="file to input")

parser.add_argument(
		"-o", "-out", "--output",
		metavar="outfile",
		dest="output",
		default = "output",
		type=str,
		help="svg file to output")

parser.add_argument(
		"-f", "-format", "--format",
		metavar="gene_info_format",
		dest="format",
		default = "auto",
		type=str,
		help="format of input file, e.g. auto, gff, simple. [default: auto]")

parser.add_argument(
		"-v", "--version",
		action='version',
		help="The version of this program.",
		version = "Version: " + __version__)
args = parser.parse_args()

tagcolors = {
	'cds': "green",
	'sts': "orange",
	'domain': "blue",
	'exon': "gold",
	'intron': "darkgrey",
	'marker': "black",
	'start_codon': "lime",
	'stop_codon': "magenta",
	'utr': "hotpink",
}

domaincolors = ["blue", "aqua", "brown", "chartreuse", "deeppink", "royalblue", "springgreen", "teal"]

tags = ['utr', 'intron', 'exon', 'cds', 'sts', 'domain' 'start_codon', 'stop_codon', 'marker']

fileform = ""
infofile=open(args.input, 'r')
data = infofile.readlines()
domain_ref = "cds"
infofile.close()
#文件格式判断
if args.format == "simple":
	fileform = "simple"
elif args.format == "gff":
	fileform = "gff"
elif args.format == "auto" or args.format not in dir():
	if re.search("\.gff$", args.format):
		fileform = "gff"
	else:
		fileform = 'simple'
else:
	print("ERROR file formate!!!")
	os._exit(0)

if fileform == "gff":
	data = Gff2Simple(data)

##绘画准备
import svgwrite
svgout = re.sub("\.svg$", "", args.output)
gspaint = svgwrite.Drawing(svgout + ".svg", (1200, 3600), debug = True)
x0 = 5
y0 = 25
paintx0=10
legendx0 = 900
legendboxx0 = legendx0 - 5

locuslist = GetLocusList(data)
for locus in locuslist:
	print("Processing gene:" , locus, "..........")
	#获取链向
	chain = GetChainOrientation(locus, data)
	#获取位置最小值、最大值
	(MinPos, MaxPos) = GetMinMax(locus, data)
	#print("Min Value: ", MinPos)
	#print("Max Value: ", MaxPos)

	Grange = MaxPos - MinPos + 1
	times = Grange / 1000

	#显示基因名
	gspaint.add(gspaint.text(
		locus,
		insert=(paintx0, y0),
		font_size = 16,
		fill = 'black'))
	y0 = y0 +60
	legendy0 = y0 + 60
	legendboxy0 = legendy0 - 5
	unit = 1000.0
	segments = Grange // unit
	#绘制链向
	if chain == '+':
		lines = gspaint.add(gspaint.g(stroke_width=2, stroke='gray', fill='none'))
		lines.add(gspaint.polyline(
		[(paintx0, y0 - 25), (paintx0 + 40, y0 - 25), (paintx0 + 40, y0 - 27.5), (paintx0 + 45, y0 - 22.5), (paintx0 + 40, y0 - 17.5), (paintx0 + 40, y0 - 20), (paintx0, y0 - 20),(paintx0, y0 - 25)]))
	else:
		lines = gspaint.add(gspaint.g(stroke_width=2, stroke='gray', fill='none'))
		lines.add(gspaint.polyline(
		[(paintx0, y0 - 22.5), (paintx0 + 5, y0 - 17.5), (paintx0 + 5, y0 - 20), (paintx0 + 45, y0 - 20), (paintx0 + 45, y0 - 25), (paintx0 + 5, y0 - 25), (paintx0 + 5, y0 - 27.5),(paintx0, y0 - 22.5)]))

		
	#绘制比例尺
	scalelen = 1000.0/Grange*1000
	gspaint.add(gspaint.line(
	((MinPos - MinPos)/times + paintx0, y0-50),
	((MaxPos - MinPos)/times + paintx0, y0-50),
	stroke_width=2,
	stroke="black"))
	i = 1
	scalex = MinPos + unit
	while i <= segments:
		gspaint.add(gspaint.line(
			((scalex - MinPos)/times + paintx0, y0-50),
			((scalex - MinPos)/times + paintx0, y0-45),
			stroke_width=1,
			stroke="gray"))
		gspaint.add(gspaint.text(
			str(i) + "k",
			insert=((scalex - MinPos)/times + paintx0 - 6, y0-35),
			font_size = 10,
			fill = 'black'))
		scalex += unit
		i += 1

	utrinfo = GetTagInfo(locus, 'utr', data)
	if len(utrinfo) > 0:
		gspaint.add(gspaint.rect(
			insert = (legendx0, legendy0+1.5),
			size = ("40px", "12px"),
			stroke_width = 0.001,
			stroke = tagcolors["utr"],
			fill = tagcolors["utr"]))
		gspaint.add(gspaint.text(
			"utr",
			insert = (legendx0 + 50, legendy0+12),
			font_size = 12,
			fill = 'black'))
		legendy0 += 25

	#paint intron
	introninfo = GetTagInfo(locus, 'intron', data)
	for info in introninfo:
		(start, end) = info.split("-")
		start = int(start)
		end = int(end)
		gspaint.add(gspaint.line(
			((start - MinPos)/times + paintx0, y0 + 7.5),
			((end - MinPos)/times + paintx0, y0 + 7.5),
			stroke_width = 2,
			stroke = tagcolors["intron"]))

	if len(introninfo) > 0:
		gspaint.add(gspaint.line(
			(legendx0, legendy0+8),
			(legendx0+40, legendy0+8),
			stroke_width = 2,
			stroke = tagcolors["intron"]))
		gspaint.add(gspaint.text(
			"intron",
			insert = (legendx0 + 50, legendy0+12),
			font_size = 12,
			fill = 'black'))
		legendy0 += 25



	#paint exon
	if fileform != "gff":
		exoninfo = GetTagInfo(locus, 'exon', data)
		for info in exoninfo:
			(start, end) = info.split("-")
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
				insert = ((begin - MinPos ) / times + paintx0, y0 - 5),
				size = (str(length) + "px", "25px"),
				stroke_width = 0.001,
				stroke = tagcolors["exon"],
				fill = tagcolors["exon"]))

		if len(exoninfo) > 0:
			gspaint.add(gspaint.rect(
				insert = (legendx0, legendy0),
				size = ("40px", "25px"),
				stroke_width = 0.001,
				stroke = tagcolors["exon"],
				fill = tagcolors["exon"]))
			gspaint.add(gspaint.text(
				"exon",
				insert = (legendx0 + 50, legendy0+16),
				font_size = 12,
				fill = 'black'))
			legendy0 += 35

	#paint utr

	for info in utrinfo:
		(start, end) = info.split("-")
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
			insert = ((begin - MinPos)/times + paintx0, y0+1.5),
			size = (str(length) + "px", "12px"),
			stroke_width = 0.001,
			stroke = tagcolors["utr"],
			fill = tagcolors["utr"]))

	#paint cds
	cdsinfo = GetTagInfo(locus, 'cds', data)
	for info in cdsinfo:
		(start, end) = info.split("-")
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
			insert = ((begin - MinPos) / times + paintx0, y0 - 5),
			size = (str(length) + "px", "25px"),
			stroke_width = 0.001,
			stroke = tagcolors["cds"],
			fill = tagcolors["cds"]))

	if len(cdsinfo) > 0:
		gspaint.add(gspaint.rect(
			insert = (legendx0, legendy0),
			size = ("40px", "25px"),
			stroke_width = 0.001,
			stroke = tagcolors["cds"],
			fill = tagcolors["cds"]))
		gspaint.add(gspaint.text(
			"CDS",
			insert = (legendx0 + 50, legendy0+16),
			font_size = 12,
			fill = 'black'))
		legendy0 += 35


	#paint sts
	stsinfo = GetTagInfo(locus, 'sts', data)
	for info in stsinfo:
		(start, end) = info.split("-")
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
			insert = ((begin - MinPos) / times + paintx0, y0 - 5),
			size = (str(length) + "px", "25px"),
			stroke_width = 0.001,
			stroke = tagcolors["sts"],
			fill = tagcolors["sts"]))

	if len(stsinfo) > 0:
		gspaint.add(gspaint.rect(
			insert = (legendx0, legendy0),
			size = ("40px", "25px"),
			stroke_width = 0.001,
			stroke = tagcolors["sts"],
			fill = tagcolors["sts"]))
		gspaint.add(gspaint.text(
			"CDS",
			insert = (legendx0 + 50, legendy0+16),
			font_size = 12,
			fill = 'black'))
		legendy0 += 35


	#paint domain
	cdsposdata = SortCDSInfo(locus, domain_ref, data)
	if cdsposdata ==[]:
		cdsposdata = SortCDSInfo(locus, "exon", data)

	domaininfo = GetDomainInfo(locus, 'domain', data)
	domainlist = []
	for line in domaininfo:
		domainlist.append(line.split("-")[0])

	domainset= list(set(domainlist))
	domainset.sort()
	domainsetcolors={}
	index = 0
	while index < len(domainset):
		domainsetcolors[domainset[index]] = domaincolors[index]
		index += 1

	for line in domaininfo:
		(domain, aa1, aa2) = line.split("-")
		aa1 = int(aa1)
		aa2 = int(aa2)
		nucl0 = aa1 * 3 - 2
		length = (aa2 - aa1 + 1) * 3
		domain2cdsinfo = Domain2CDS(nucl0, length, cdsposdata)
		domainsave=[];
		for info in domain2cdsinfo:
			(start, end) = info.split("-")
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
				insert = ((begin - MinPos) / times + paintx0, y0 - 5),
				size = (str(length) + "px", "25px"),
				stroke_width = 0.01,
				stroke = domainsetcolors[domain],
				fill = domainsetcolors[domain]))
			if domain not in domainsave:
				gspaint.add(gspaint.rect(
					insert = (legendx0, legendy0),
					size = ("40px", "25px"),
					stroke_width = 0.001,
					stroke = domainsetcolors[domain],
					fill = domainsetcolors[domain]))
				gspaint.add(gspaint.text(
					domain,
					insert = (legendx0 + 50, legendy0+16.5),
					font_size = 12,
					fill = 'black'))
				legendy0 += 35
				domainsave.append(domain)
	legendy0 -= 5
	lines = gspaint.add(gspaint.g(stroke_width=2, stroke='gray', fill='none'))
	lines.add(gspaint.polyline(
		[(legendboxx0, legendboxy0), (1010, legendboxy0), (1010, legendy0), (legendboxx0, legendy0), (legendboxx0, legendboxy0)]))


	#paint start codon
	stcodoninfo = GetTagInfo(locus, 'start_codon', data)
	for info in stcodoninfo:
		(start, end) = info.split("-")
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
			insert = ((begin - MinPos) / times + paintx0, y0 - 12.5),
			size = (str(length) + "px", "40px"),
			stroke_width = 0.001,
			stroke = tagcolors["start_codon"],
			fill = tagcolors["start_codon"]))
		gspaint.add(gspaint.text(
			"ATG",
			insert = ((begin - MinPos) / times + paintx0 - 10, y0 + 42),
			font_size = 10,
			fill = 'black'))

	#paint end codon
	endcodoninfo = GetTagInfo(locus, 'stop_codon', data)
	for info in endcodoninfo:
		(start, end) = info.split("-")
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
			insert = ((begin - MinPos)/times - 2 + paintx0, y0 - 12.5),
			size = (str(length) + "px", "40px"),
			stroke_width = 0.001,
			stroke = tagcolors["stop_codon"],
			fill = tagcolors["stop_codon"]))
		gspaint.add(gspaint.text(
			"TAG",
			insert = ((begin - MinPos) / times - 10 + paintx0, y0 + 42),
			font_size = 10,
			fill = 'black'))

	#paint marker
	markerinfo = GetDomainInfo(locus, 'marker', data)
	for info in markerinfo:
		(marker, start, end) = info.split("-")
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
			insert = ((begin - MinPos)/times - 2 + paintx0, y0 - 12.5),
			size = (str(length) + "px", "40px"),
			stroke_width = 0.001,
			stroke = tagcolors["marker"],
			fill = tagcolors["marker"]))
		gspaint.add(gspaint.text(
			marker,
			insert = ((begin - MinPos) / times - 10 + paintx0, y0 -20),
			font_size = 10,
			fill = 'red'))

	y0 = legendy0 + 50

gspaint.save()

print("\nThe outfile:\n" + svgout + ".svg")
print("""
-------------------------
Success!!!
Congratulations to you!!!
-------------------------"""
)


