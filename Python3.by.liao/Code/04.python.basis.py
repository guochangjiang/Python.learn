#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# print absolute value of an integer:
a = 100
if a >= 0:
    print(a)
else:
    print(-a)

## \转义
str = 'I\'m \"OK\"!'
print(str)
print('I\'m learning\nPython.')
print("I\'m learning\nPython.")
print("I'm learning\nPython.")

## r''取消转义
print('\\\t\\')
print(r'\\\t\\')
a = r'I\'m "OK"'
print(a)

##多行```...```
print("多行")
print('''line1
line2
line3''')
a = '''line1
line2'''
print(a)

print(r'''line1\n
line2\n
line3''')

##Boole运算
print(3 > 5)
print(3 < 5)
print(5 > 3 and 3 > 1)
print(5 > 3 and 3 < 1)
print(5 > 3 or 3 < 1)
print(not 1 > 2)

age=25
if age >= 18:
    print('adult')
else:
    print('teenager')

##变量
a = 123
print(a)
a = 'ABC'
print(a)
b = 'XYZ'
print(a,b)
a, b = b, a
print(a,b)

##常量
PI=3.141592653

##除法
print(9/3)
print(10/3)
print(10//3)
print(10%3)

##练习
n = 123
f = 456.789
s1 = 'Hello, world'
s2 = 'Hello, \'Adam\''
s3 = r'Hello, "Bart"'
s4 = r'''Hello,
Lisa!'''
print(n,f,s1,s2,s3,s4)

##编码相关函数
print(ord('A')) ## 65
print(ord('中')) ## 20013

print(chr(65))
print(chr(ord('A')))
print(chr(ord('中')))

print('\u4e2d\u6587') ## '中文'的十六进制编码

## bytes类型数据b'',encode(),decode()
x = b'ABC'
print(x)
print(x.decode('ascii'))

print('ABC'.encode('ascii'))
print('中文'.encode('utf-8'))
#print('中文'.encode('ascii'))  ##error
print(b'\xe4\xb8\xad\xe6\x96\x87'.decode('utf-8'))

## 字符串长度len()
print(len('ABC'))
print(len('中文'))
print(len(b'ABC'))
print(len('中文'.encode('utf-8')))


## 格式化输出
print('Hello, %s' % 'world!')
print('Hi, %s, you have $%d.' % ('Michael', 100000))
print('%2d--%02d' % (3,1))
print('%.2f' % 3.1415926)
print('Age: %s. Gender: %s' % (25,True))
print('growth rate: %d %%' % 7)

s1 = 72
s2 = 85
r=(85-72)*100/72
print('improved %.1f %%' % r)

## 列表
classmates = ['Michael', 'Bob', 'Tracy']
print('classmates')
print(classmates)
print(len(classmates))
print(classmates[0])
print(classmates[1])
print(classmates[2])
print(classmates[-1])
classmates.append('Adam') #向末尾添加元素
print(classmates[-1])
classmates.insert(1,'Jack') #向指定位置插入元素
print(classmates[1])
del_ele = classmates.pop() #删除末尾元素
print(del_ele)
classmates.pop(0) #删除知道你敢位置的元素
print(classmates)
classmates[0]='Sarah' #替换元素
print(classmates)

s1 = ['Python', 'java', 123] #不同类型元素
s2 = ['python', 'java', ['asp', 'php'], 'perl'] #元素可以是列表（嵌套）
print(s2[2][0])

##元组
s3 = ('python', 'perl', 'java') #元组，不可更改

##条件判断： if语句
age = 20
if age >= 18:
    print('adult')
elif age >= 6:
    print('teenager')
else:
    print('kid')

birth = input('birth: ')  ##input的返回数据类型为str
birth = int(birth)
if birth < 2000:
	print('00前')
else:
	print('00后')

## 循环 for语句和while语句
sum = 0
for x in [1,2,3,4,5]:
	sum = sum + x
print(sum)
sum = 0
for x in range(101): #1-100
	sum = sum + x
print(sum)

sum = 0
n = 99
while n > 0:
	sum = sum + n
	n = n - 2
print(sum)

## 字典dict
d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
print(d['Bob'])


