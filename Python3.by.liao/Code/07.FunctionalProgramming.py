#!/usr/bin/env python3
# --*-- utf-8 --*--

##变量指向函数
f = abs
print(abs(-10))
a = f(-10)
print(a)

##函数名也是变量
max = 11  #max函数功能失效
print(max)

##高阶函数
def add(x, y, f):
    return f(x) + f(y)
print(add(-15, -6, abs))

