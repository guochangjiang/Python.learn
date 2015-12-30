#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#===============================================================================
#
#         FILE: Get.GFF.by.gene.list.v.1.0.py
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
#      CREATED: 2015/12/22 14:27:55
#       UPDATE: 2015/12/22 14:27:55
#===============================================================================
#   Change logs:
#   Version

import re

__version__ = '1.0'

genelist = []

genelistfile = open("genelist", "r")
for line in genelistfile:
    line = line.strip()
    if line == '':
        continue
    line = re.sub("\.\d+$", "", line)
    genelist.append(line)
genelistfile.close()

gfffile = open(".gff", "r")
for line in gfffile:
    line = line.strip()
    if line == '':
        continue
    columns = line.split()
    if columns[2] == "gene":
        m = re.search("^\w+=([a-zA-Z_0-9]+)", columns[-1])
        genelocus = m.group(1)
        if genelocus in genelist:
            print(line)
    else:
        m = re.search("^\w+=([0-9a-zA-Z_]+\.\d+)", columns[-1])
        genelocus = m.group(1)
        if genelocus in genelist and re.search("\.1$", genelocus):
            print(line)
gfffile.close()


