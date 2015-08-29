#!/usr/bin/env python3
# --*-- utf-8 --*--

##切片
L = ['Michael', 'Sarah', 'Tracy', 'Bob', 'Jack']
print(L[0:3])
print(L[:3])
print(L[-2:])
print(L[:])

L = list(range(100))  #0-99
print(L[:10])
print(L[-10:])
print(L[10:20])
print(L[:10:2])
print(L[::10])
#元组切片
L = (0, 1, 2, 3, 4, 5)
print(L[:3])
#字符串切片
print('ABCDEFG'[:3])
print('ABCDEFG'[::2])

##迭代

#列表迭代
L = [1, 2, 3, 4, 5]
for x in L:
    print(x)
#字符串迭代
for s in 'UVWXYZ':
    print(s)
#字典迭代
d = {'a': 1, 'b': 2, 'c': 3}
for key in d:
    print(key)
for value in d.values():
    print(value)
for k, v in d.items():
    print(k, v)
#迭代对象判断
from collections import Iterable
print(isinstance('abc', Iterable))
print(isinstance([1, 2, 3], Iterable))
print(isinstance(d, Iterable))
print(isinstance(123, Iterable))

#列表下标循环的实现
for i, value in enumerate(['a', 'b', 'c']):
    print(i, value)

##列表生成式
print([x * x for x in range(1, 11)])
print([x * (x-1) for x  in range(1, 11)])
print([x * x for x in range(1, 11) if x % 2 == 0])
print([m + n for m in 'ABC' for n in 'XYZ'])
#列出当前目录下的所有文件和目录名
import os
print([d for d in os.listdir('.')])
#
d = {'a': 'A', 'b': 'B', 'c': 'C'}
print([k + '=' + v for k, v in d.items()])

#把列表中的字符串小写
print([s.lower() for s in ['Hello', 'World', 'IBM', 'Apple']])

##练习
L= ['Hello', 'World', 18, 'IBM', 'Apple']
print([s.lower() for s in L if isinstance(s, str)])

##生成器
L = [x * x for x in range(10)]
print(L)
g = (x * x for x in range(10))
print(next(g))
for n in g:
    print(n)
def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        print(b)
        a, b = b, a+b
        n = n + 1
    return 'done'
fib(6)
def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a+b
        n = n + 1
    return 'done'
f = fib(6)
for n in f:
    print(n)

while True:
    try:
        x = next(f)
        print('f:', x)
    except StopIteration as e:
        print('Generator return value:', e.value)
        break

def triangles():
    a = [1]
    while True:
        yield a
        a = [sum(i) for i in zip([0] + a, a + [0])]

n = 0
for t in triangles():
    print(t)
    n = n + 1
    if n == 10:
        break

## 可迭代对象判断
print(isinstance([], Iterable))
print(isinstance({}, Iterable))
print(isinstance('abc', Iterable))
print(isinstance(100, Iterable))

##迭代器对象判断
print(isinstance([], Iterator))
print(isinstance(iter([]), Iterator))
print(isinstance({}, Iterator))
print(isinstance((x for x in range(10)), Iterator))


