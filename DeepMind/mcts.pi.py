#!/usr/bin/env python3
#-*- coding: utf-8 -*-

'''
蒙特卡洛模拟求Pi
'''

import random

def M_C(num):
    count = 0
    print(num)
    for i in range(1, num+1):
        #print(i)
        X = random.uniform(0,1)
        Y = random.uniform(0,1)
        if X**2 + Y**2 < 1:
            count += 1
    return 4.0 * count/num

if __name__ == "__main__":
    print(M_C(10000000))