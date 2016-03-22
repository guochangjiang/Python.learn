#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys

fastafile = sys.argv[1]
len_dict = {}

with open(fastafile) as TMP:
    for line in TMP:
        line = line.strip()
        if line == "":
            continue
        if line[0] == ">":
            name = line.replace(">","")
            len_dict[name] = 0
        else:
            len_dict[name] += len(line)

for key in sorted(len_dict.keys()):
    print("%s\t%d\n" % (key, len_dict[key]))