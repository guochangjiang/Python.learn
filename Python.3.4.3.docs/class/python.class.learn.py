#!/usr/bin/env python3
# --*-- utf-8 --*--
#
#===============================================================================
#
#         FILE: python.class.learn.py
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
#      CREATED: 2015/10/28 20:52:22
#       UPDATE:
#===============================================================================
#   Change logs:
#   Version

__version__ = '1.0'

class Student(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score
    def print_score(self):
        print('%s: %s' % (self.name, self.score))
    def get_grade(self):
        if self.score >= 90:
            return 'A'
        elif self.score >= 60:
            return 'B'
        else:
            return 'C'

listclass=[]
bart=Student('Bart Simpson', 59)
listclass.append(bart)
print(listclass[0].name)
print(listclass[0].score)
print(listclass[0].get_grade())

class ChrBlock(object):
    def __init__(self, chrname, blockname, data):
        self.chrname = chrname
        self.blockname = blockname
        self.data = data
