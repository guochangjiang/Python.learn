#!/usr/bin/python3
# coding=utf-8

import sqlite3

#连接数据库
conn = sqlite3.connect('test.db')
print("Opened database successfully")

#创建新表
conn.execute('''CREATE TABLE if not exists COMPANY
       (ID INT PRIMARY KEY     NOT NULL,
       NAME           TEXT    NOT NULL,
       AGE            INT     NOT NULL,
       ADDRESS        CHAR(50),
       SALARY         REAL);''')
print("Table created successfully")

conn.close()

conn = sqlite3.connect('test.db')
cu=conn.cursor()
print("Opened database successfully")

#插入新数据
cu.execute("Select * from COMPANY where NAME = ? OR ID = ?", ('Paul2', 5 ))
check1=cu.fetchone()
if check1 == None:
    conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
        VALUES (5, 'Paul2', 32, 'California', 20000.00 )")

cu.execute("Select * from COMPANY where NAME = ? OR ID = ?", ('Allen', 2 ))
check1=cu.fetchone()
if check1 == None:
    conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
        VALUES (2, 'Allen', 25, 'Texas', 15000.00 )")

cu.execute("Select * from COMPANY where NAME = ? OR ID = ?", ('Teddy', 3 ))
check1=cu.fetchone()
if check1 == None:
    conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
        VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )")

cu.execute("Select * from COMPANY where NAME = ? OR ID = ?", ('Mark', 4 ))
check1=cu.fetchone()
if check1 == None:
    conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
        VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )")



conn.commit()
print("Records created successfully")

#读取条目
cursor = conn.execute("SELECT id, name, address, salary  from COMPANY")
for row in cursor:
    print ("ID = ", row[0])
    print ("NAME = ", row[1])
    print ("ADDRESS = ", row[2])
    print ("SALARY = ", row[3], "\n")

print ("Operation done successfully")

#更新数据
conn.execute("UPDATE COMPANY set SALARY = 25000.00 where ID=1")
x="长江"
updatecn = "UPDATE COMPANY set NAME = \"%s\" where ID=4" % x

conn.execute("UPDATE COMPANY set NAME = \"中国\" where ID=5")
conn.execute(updatecn)
conn.commit()
print("Total number of rows updated :", conn.total_changes)

#删除数据
conn.execute("DELETE from COMPANY where ID=2")
conn.commit()
print ("Total number of rows deleted :", conn.total_changes)
conn.close()