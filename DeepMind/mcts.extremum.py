#!/usr/bin/env python3
#-*- coding: utf-8 -*-

'''
蒙特卡洛模拟求函数极值
'''

import numpy as np
import random

ymax = 0
y = lambda x:200*np.sin(x)*np.exp(-0.05*x)
num = int(input(u'请输入模拟次数：'))
for i in range(1, num+1):
    x0 = random.uniform(-2,2)
    if y(x0)>ymax:
        xmax = x0
        ymax = y(x0)
print(ymax)