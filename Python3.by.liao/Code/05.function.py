#!/usr/bin/env python3
# --*-- utf-8 --*--

## 一些内置函数
print(abs(-20))  #abs只能有一个int或float型参数
print(max(2, 3, 4, 5))
print(min(2, 3, 4, 5))

## 数据类型转换
print('123 to int:', int ('123'))
# print('123.123 to int:', int ('123.123')) #error
print(123.123, 'to int:', int(123.123) )
print('123.123 to float:', float('123.123'))
print(123.123,'to str:', str(123.123))
print(1, 'to bool:', bool(1))
print("'' to bool:", bool(''))

## 函数名赋值
a = abs
print(a(-1))

## 练习：将十进制转换为十六进制
n1 = 255
n2 = 1000
print(hex(n1))
print(hex(n2))

##空函数
def nop():
    pass

##参数检查
def my_abs(x):
    if not isinstance(x,(int, float)):
        raise TypeError('bad operand type')
    if x >= 0:
        return x
    else:
        return -x
#print(my_abs('A'))
#print(abs('A'))

##返回多个值
import math
def move(x,y,step,angle=0):
    nx = x + step * math.cos(angle)
    ny = y - step * math.sin(angle)
    return nx, ny
x, y = move(100, 100, 60, math.pi / 6)
print(x, y)

##练习：求一元二次方程的两个根
def quadratic(a, b, c):
    x1 = math.sqrt((b*b-4*a*c)/4/a/a) - b * 0.5 / a
    x2 = 0 - math.sqrt(b**2/4/a/a - c/a) - b * 0.5 / a
    return x1,x2

x1, x2 = quadratic(1,2,-1)
print(x1, x2)

##位置参数
def power(x, n):
    s = 1
    while n > 0:
        n = n - 1
        s = s * x
    return s

print(power(5, 3))

##默认参数
def power(x, n=2):
    s = 1
    while n > 0:
        n = n - 1
        s = s * x
    return s

print(power(5))
print(power(5, 2))

def enroll(name, gender, age=6, city='Beijing'):
    print('name:', name)
    print('gender:', gender)
    print('age:', age)
    print('city:', city)

enroll('Bob', 'M', 7)
enroll('Adam', 'M', city='Tianjin')

##可变参数
def calc(numbers):  #需要先组装出list或tuple
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum
print(calc([1,2,3]))
print(calc((1,3,5,7)))

def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum
print(calc(1, 2, 3))
num = [1, 2, 3]
print(calc(*num))

##关键字参数
def person(name, age, **kw):
    print('name:', name, 'age:', age, 'other:', kw)
person('Michaeal', 30)
person('Bob', 35, city='Beijing')
person('Adam', 45, gender='M', job='Engineer')
extra = {'city': 'Beijing', 'job': 'Engineer'}
person('Jack', 24, city=extra['city'], job=extra['job'])
person('Jack', 24, **extra)

##命名关键字参数
def person(name, age, *, city='Beijing', job):
    print(name, age, city, job)

person('Jack', 24, city='Beijing', job='Engineer')

##参数组合
def f1(a, b, c=0, *args, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kw)

f1(1,2)
f1(1, 2, 3, 'a', 'b')
f1(1, 2, 3, 'a', 'b', x=99)
args = (1, 2, 3, 4, 5)
kw = {'d': 99, 'x': '#'}
f1(*args, **kw)

##递归函数
def fact(n):
    if n ==1:
        return 1
    return n * fact(n - 1)
print(fact(5))
#汉诺塔
def move(n, a, b, c):
    if n == 1:
        print('# move', a, '-->', c) #直接移动
        return
    move(n-1, a, c, b)                  # 将前n-1个盘子从a借助c移动到b上
    print('# move', a, '-->', c)  # 将a上最底下的盘子移动到c上
    move(n-1, b, a, c)                  # 将b上的n-1个盘子借助a移动到c上
move(4, 'A', 'B', 'C')
# move(64, 'A', 'B', 'C')

