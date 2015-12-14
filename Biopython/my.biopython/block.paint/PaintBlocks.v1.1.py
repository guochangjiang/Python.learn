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
#      VERSION: 1.1
#      CREATED: 2015/10/26 15:41:47
#       UPDATE: 2015/10/27 14:26:00
#===============================================================================
#   Change logs:
#   Version 1.0 2015/10/26: 初始版本，可支持多chr多block，但未合并相邻的相同type区域
#   Version 1.1 2015/10/27: 加入type合并功能，新增参数：最小色块的长度(步长)与宽度，
#                           block之间间距，染色体间距参数，长度单位(bp/aa)
#                           新增图例显示，比例尺显示

__version__ = '1.1'

import argparse
import svgwrite


##参数处理
parser = argparse.ArgumentParser(
    description="Version: " + __version__,
    epilog="Please Enjoy this Program!")
parser.add_argument(
    "-i", "-in", "--input",
    metavar="blockfile",
    dest="input",
    type=str,
    help="Block file to paint")
parser.add_argument(
    "-prefix", "--prefix",
    metavar="outname",
    dest="prefix",
    default = "out",
    type=str,
    help="output SVG file name prefix [default: out]")
parser.add_argument(
    "-C", "--color",
    metavar="colors",
    dest="colors", type=str,
    help="specify colors for certain block types, in the format:\n\t\"type1:color1;type2:color2;...\"")
parser.add_argument(
    "-S", '-step', "--step", "-length", "--length",
    metavar="step_size",
    dest="step",
    default=0.5,
    type=int,
    help="minimum length of rectangle or step size of rectangle movment [default: 0.5px]")
parser.add_argument(
    "-width", "--width", "-height", "-thickness",
    metavar="Block_height",
    dest="width",
    type=int,
    default=25,
    help="length of rectangle [default: 25px]")
parser.add_argument(
    "-bd", "--block-distance",
    metavar="Block_distance",
    dest="block_distance",
    type=int, default=10,
    help="distance of adjacent blocks [default: 10px]")
parser.add_argument(
    "-cd", "--chromosome-distance",
    metavar="Chromosome_distance",
    dest="chr_distance",
    type=int,
    default=30,
    help="distance of adjacent blocks [default: 30px]")
parser.add_argument(
    "-u", "--unit",
    metavar="unit",
    dest="unit",
    type=str,
    default="bp",
    help="unit of type [default: aa]")
parser.add_argument(
    "-v", "--version",
    action='version',
    help="The version of this program.",
    version = "Version: " + __version__)
args = parser.parse_args()

##颜色处理
colors={}
for pair in args.colors.split(";"):
    cpair = pair.split(":")
    colors[cpair[0]] = cpair[1]

##数据读取
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


##SVG图像绘画
outsvg = args.prefix + ".svg"
dwg = svgwrite.Drawing(outsvg, debug=True)

x0 = 5
y0 = 15
chrx0 = 5
blockx0 = 50
rectx0 = 120
sw=args.width / 100
dwg.add(dwg.text(
    "chr",
    insert=(chrx0, y0),
    font_size = 16,
    fill='black'))
dwg.add(dwg.text(
    "block",
    insert=(blockx0, y0),
    font_size = 16,
    fill='black'))
dwg.add(dwg.text(
    "type figure",
    insert=(rectx0, y0),
    font_size = 16,
    fill='black'))
y0+=15

def MergeType(type_ori):
    type_mer=[]
    i=0
    count=1
    #print("\n",len(type_ori))
    while i < len(type_ori)-1:
        if type_ori[i] == type_ori[i+1]:
            count += 1
            i = i + 1
            if i+1 == len(type_ori)-1:
                type_mer.append(type_ori[i])
                type_mer.append(count)
                break
        elif type_ori[i] != type_ori[i+1]:
            type_mer.append(type_ori[i])
            type_mer.append(count)
            count=1
            i = i +1

    if type_ori[-2] != type_ori[-1]:
        type_mer.append(type_ori[-1])
        type_mer.append(1)
        #print("type_ori[-1]:", type_ori[-1])
        #print("type_ori[-2]:", type_ori[-2])
    #print(type_ori)
    #print(type_mer)
    return type_mer

print()
for chr in sorted(ChrDict.keys()):
    print("Painting chr", chr, "...........", end='')
    blocknum = len(ChrDict[chr])
    currenty = y0
    chry0 = y0 + (blocknum * (args.width+args.block_distance) / 2)
    dwg.add(dwg.text(
                    chr,
                    insert=(chrx0, chry0),
                    font_size = 14,
                    fill='black'))
    for block in sorted(BloDict.keys()):
        blochr = block.split("#")
        if blochr[1] == chr:
            print("\n\tPainting block", block, ".........", end='')
            dwg.add(dwg.text(
                blochr[0],
                insert=(blockx0, currenty+15),
                font_size = 14, fill='black'))
            currentx = rectx0
            btype = MergeType(BloDict[block])
            index = 0
            while index < len(btype)-1:
                length = btype[index+1] * args.step
                dwg.add(dwg.rect(
                    insert=(currentx, currenty),
                    size = (str(length) + "px", str(args.width) + "px"),
                    stroke_width = sw,
                    stroke = colors[btype[index]],
                    fill = colors[btype[index]]))
                currentx += length
                index += 2
            currenty += (args.width + args.block_distance)
    y0 = currenty + args.chr_distance - args.block_distance
    print("\n")

## 比例尺显示
y0 = y0 +10
dwg.add(dwg.text(
    "scale",
    insert=(blockx0, y0+10),
    font_size = 14,
    fill='black'))
dwg.add(dwg.line(
    (rectx0, y0+10),
    (rectx0+100*args.step, y0+10),
    stroke_width=2,
    stroke="black"))
dwg.add(dwg.line(
    (rectx0+1, y0+10),
    (rectx0+1, y0+7),
    stroke_width=2,
    stroke="black"))
dwg.add(dwg.line(
    (rectx0+100*args.step-1, y0+10),
    (rectx0+100*args.step-1, y0+7),
    stroke_width=2,
    stroke="black"))
dwg.add(dwg.text(
    "100" + str(args.unit),
    insert=(rectx0+4, y0+5),
    font_size = 14,
    fill='black'))


##图例生成
y0 = y0 + args.width + args.block_distance
print("\nPainting legend............", end='')
dwg.add(dwg.text(
    "legend",
    insert=(chrx0, y0+10),
    font_size = 14,
    fill='black'))
for type in sorted(colors.keys()):
    print("\n\tpaint type", type, "..............", end='')
    y0 = y0 + args.width + args.block_distance
    dwg.add(dwg.rect(
        insert=(blockx0, y0),
        size = ("25px", str(args.width) + "px"),
        stroke_width = sw,
        stroke = colors[type],
        fill = colors[type]))
    dwg.add(dwg.text(
        type,
        insert=(blockx0 + 30, y0 + (args.width/1.5)),
        font_size = 12,
        fill = "black"))

dwg.save()
print("""
\n\n-------------------------
Success!!!
Congratulations to you!!!"""
)

