#!/usr/bin/env python3
# --*-- utf-8 --*--
#
#===============================================================================
#
#         FILE: PaintBlocks.v1.0.py
#
#        USAGE: usage
#
#  DESCRIPTION: 将输入的block信息（格式见example.blocks1.txt)根据类型信息进行SVG绘图
#
#      OPTIONS: -in blocks.info.file -prefix <prefixofoutputSVG>
# REQUIREMENTS:
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: Guo Changjiang (polaris), guochangjiang1989@gmail.com
# ORGANIZATION: Nanjing University, China
#      VERSION: 1.0
#      CREATED: 2015/10/26 15:41:47
#       UPDATE:
#===============================================================================
#   Change logs:
#   Version 1.0 2015/10/26: 初始版本，可支持多chr多block，但未合并相邻的相同type区域

__version__ = '1.0'

import argparse
import svgwrite

parser = argparse.ArgumentParser(description="Version: " + __version__, epilog="Please Enjoy this Program!")
parser.add_argument("-i", "-in", "--input", metavar="blockfile", dest="input", type=str, help="Block file to paint")
parser.add_argument("-prefix", "--prefix", metavar="outname", dest="prefix", default = "out", type=str, help="output SVG file name prefix, default: out")
parser.add_argument("-C", "--color", metavar="colors", dest="colors", type=str, help="specify colors for certain block types, in the format:\n\t\"type1:color1;type2:color2;...\"")
parser.add_argument("-v", "--version", action='version', help="The version of this program.", version = "Version: " + __version__)
args = parser.parse_args()

##colors
colors={}
for pair in args.colors.split(";"):
    cpair = pair.split(":")
    colors[cpair[0]] = cpair[1]

Blockfile = open(args.input, "r")
ChrDict = {}
BloDict = {}
chrarray = []
for line in Blockfile:
    line = line.strip("\n")
    if line[0] == "#" or line[0] == "":
        continue
    data = line.split("\t")
    bloname = data[0]
    chrname = data[1]
    if chrname not in chrarray:
        chrarray.append(chrname)
        ChrDict[chrname]=[];
    ChrDict[chrname].append(bloname)
    blochr = bloname + '#' + chrname
    BloDict[blochr]=data[2:]

Blockfile.close()

outsvg = args.prefix + ".svg"
dwg = svgwrite.Drawing(outsvg, (700, 700), debug=True)

x0 = 0
y0 = 0
chrx0 = 0
blockx0 = 100
rectx0 = 200
dwg.add(dwg.text("chr", insert=(chrx0, -30), font_size = 16, fill='black'))
dwg.add(dwg.text("block", insert=(blockx0, -30), font_size = 16, fill='black'))
dwg.add(dwg.text("type figture", insert=(rectx0, -30), font_size = 16, fill='black'))

for chr in sorted(ChrDict.keys()):
    blocknum = len(ChrDict[chr])
    currenty = y0
    chry0 = y0 + (blocknum * 45 / 2)
    dwg.add(dwg.text(chr, insert=(chrx0, chry0), font_size = 14, fill='black'))
    for block in sorted(BloDict.keys()):
        blochr = block.split("#")
        if blochr[1] == chr:
            dwg.add(dwg.text(blochr[0], insert=(blockx0, currenty+15), font_size = 10, fill='black'))
            currentx = rectx0
            btype = BloDict[block]
            for type in btype:
                dwg.add(dwg.rect(insert=(currentx, currenty), size = ("0.60px", "30px"), stroke_width = 0.005, stroke = colors[type], fill = colors[type]))
                currentx += 0.60
            currenty += 45
    y0 = currenty + 45

dwg.save()

