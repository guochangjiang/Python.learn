#!/usr/bin/env python3
#-*- coding: utf-8 -*-

list1 = []
list2 = []
with open("list1.txt",'rb') as LIST:
    for line in LIST:
        line = line.decode('utf-8')
        line = line.strip()
        if line == "":
            continue
        list1.append(line)
with open("list2.txt", 'rb') as LIST:
    for line in LIST:
        line = line.decode('utf-8')
        line = line.strip()
        if line == "":
            continue
        list2.append(line)

list1 = set(list1)
list2 = set(list2)

list3 = list1 - list2
list4 = list1 & list2

list3 = sorted(list3)
OUT = open("list3.txt", "w")
for name in list3:
   OUT.write(name + "\n")

for name in list4:
    print(name)