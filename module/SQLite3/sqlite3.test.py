import sqlite3
cx = sqlite3.connect("test.db")
#con = sqlite3.connect(":memory:")
cu=cx.cursor()
cu.execute("create table catalog (id integer primary key,pid integer,name varchar(10) UNIQUE,nickname text NULL)")

#添加
try:
    for t in[(0,10,'abc','Yu'),(1,20,'cba','Xu')]:
        cx.execute("insert into catalog values (?,?,?,?)", t)
except:
    pass

cx.commit()

#查询
print(cu.execute("select * from catalog"))
cu.fetchone()

#修改
cu.execute("update catalog set name='Boy' where id = 0")
cx.commit()

#删除
cu.execute("delete from catalog where id = 1")  
cx.commit()

#使用中文
x=u'鱼'
cu.execute("update catalog set name=? where id = 0",x)
cu.execute("select * from catalog")
cu.fetchall()

for item in cu.fetchall():
    for element in item:
        print(element)

