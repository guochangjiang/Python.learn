 #python sqlite
  2 
  3 #Author : Hongten
  4 #MailTo : hongtenzone@foxmail.com
  5 #QQ     : 648719819
  6 #Blog   : http://www.cnblogs.com/hongten
  7 #Create : 2013-08-09
  8 #Version: 1.0
  9 
#DB-API 2.0 interface for SQLite databases

import sqlite3
import os
'''SQLite数据库是一款非常小巧的嵌入式开源数据库软件，也就是说
没有独立的维护进程，所有的维护都来自于程序本身。
在python中，使用sqlite3创建数据库的连接，当我们指定的数据库文件不存在的时候
连接对象会自动创建数据库文件；如果数据库文件已经存在，则连接对象不会再创建
数据库文件，而是直接打开该数据库文件。
    连接对象可以是硬盘上面的数据库文件，也可以是建立在内存中的，在内存中的数据库
    执行完任何操作后，都不需要提交事务的(commit)

    创建在硬盘上面： conn = sqlite3.connect('c:\\test\\test.db')
    创建在内存上面： conn = sqlite3.connect('"memory:')

    下面我们一硬盘上面创建数据库文件为例来具体说明：
    conn = sqlite3.connect('c:\\test\\hongten.db')
    其中conn对象是数据库链接对象，而对于数据库链接对象来说，具有以下操作：

        commit()            --事务提交
        rollback()          --事务回滚
        close()             --关闭一个数据库链接
        cursor()            --创建一个游标

    cu = conn.cursor()
    这样我们就创建了一个游标对象：cu
    在sqlite3中，所有sql语句的执行都要在游标对象的参与下完成
    对于游标对象cu，具有以下具体操作：

        execute()           --执行一条sql语句
        executemany()       --执行多条sql语句
        close()             --游标关闭
        fetchone()          --从结果中取出一条记录
        fetchmany()         --从结果中取出多条记录
        fetchall()          --从结果中取出所有记录
        scroll()            --游标滚动

'''

#global var
#数据库文件绝句路径
DB_FILE_PATH = ''
#表名称
TABLE_NAME = ''
#是否打印sql
SHOW_SQL = True

def get_conn(path):
    '''获取到数据库的连接对象，参数为数据库文件的绝对路径
    如果传递的参数是存在，并且是文件，那么就返回硬盘上面改
    路径下的数据库文件的连接对象；否则，返回内存中的数据接
    连接对象'''
    conn = sqlite3.connect(path)
    if os.path.exists(path) and os.path.isfile(path):
        print('硬盘上面:[{}]'.format(path))
        return conn
    else:
        conn = None
        print('内存上面:[:memory:]')
        return sqlite3.connect(':memory:')

def get_cursor(conn):
    '''该方法是获取数据库的游标对象，参数为数据库的连接对象
    如果数据库的连接对象不为None，则返回数据库连接对象所创
    建的游标对象；否则返回一个游标对象，该对象是内存中数据
    库连接对象所创建的游标对象'''
    if conn is not None:
        return conn.cursor()
    else:
        return get_conn('').cursor()

###############################################################
####            创建|删除表操作     START
###############################################################
def drop_table(conn, table):
    '''如果表存在,则删除表，如果表中存在数据的时候，使用该
    方法的时候要慎用！'''
    if table is not None and table != '':
        sql = 'DROP TABLE IF EXISTS ' + table
        if SHOW_SQL:
            print('执行sql:[{}]'.format(sql))
        cu = get_cursor(conn)
        cu.execute(sql)
        conn.commit()
        print('删除数据库表[{}]成功!'.format(table))
        close_all(conn, cu)
    else:
        print('the [{}] is empty or equal None!'.format(sql))

def create_table(conn, sql):
100     '''创建数据库表：student'''
101     if sql is not None and sql != '':
102         cu = get_cursor(conn)
103         if SHOW_SQL:
104             print('执行sql:[{}]'.format(sql))
105         cu.execute(sql)
106         conn.commit()
107         print('创建数据库表[student]成功!')
108         close_all(conn, cu)
109     else:
110         print('the [{}] is empty or equal None!'.format(sql))
111 
112 ###############################################################
113 ####            创建|删除表操作     END
114 ###############################################################
115 
116 def close_all(conn, cu):
117     '''关闭数据库游标对象和数据库连接对象'''
118     try:
119         if cu is not None:
120             cu.close()
121     finally:
122         if cu is not None:
123             cu.close()
124 
125 ###############################################################
126 ####            数据库操作CRUD     START
127 ###############################################################
128 
129 def save(conn, sql, data):
130     '''插入数据'''
131     if sql is not None and sql != '':
132         if data is not None:
133             cu = get_cursor(conn)
134             for d in data:
135                 if SHOW_SQL:
136                     print('执行sql:[{}],参数:[{}]'.format(sql, d))
137                 cu.execute(sql, d)
138                 conn.commit()
139             close_all(conn, cu)
140     else:
141         print('the [{}] is empty or equal None!'.format(sql))
142 
143 def fetchall(conn, sql):
144     '''查询所有数据'''
145     if sql is not None and sql != '':
146         cu = get_cursor(conn)
147         if SHOW_SQL:
148             print('执行sql:[{}]'.format(sql))
149         cu.execute(sql)
150         r = cu.fetchall()
151         if len(r) > 0:
152             for e in range(len(r)):
153                 print(r[e])
154     else:
155         print('the [{}] is empty or equal None!'.format(sql)) 
156 
157 def fetchone(conn, sql, data):
158     '''查询一条数据'''
159     if sql is not None and sql != '':
160         if data is not None:
161             #Do this instead
162             d = (data,) 
163             cu = get_cursor(conn)
164             if SHOW_SQL:
165                 print('执行sql:[{}],参数:[{}]'.format(sql, data))
166             cu.execute(sql, d)
167             r = cu.fetchall()
168             if len(r) > 0:
169                 for e in range(len(r)):
170                     print(r[e])
171         else:
172             print('the [{}] equal None!'.format(data))
173     else:
174         print('the [{}] is empty or equal None!'.format(sql))
175 
176 def update(conn, sql, data):
177     '''更新数据'''
178     if sql is not None and sql != '':
179         if data is not None:
180             cu = get_cursor(conn)
181             for d in data:
182                 if SHOW_SQL:
183                     print('执行sql:[{}],参数:[{}]'.format(sql, d))
184                 cu.execute(sql, d)
185                 conn.commit()
186             close_all(conn, cu)
187     else:
188         print('the [{}] is empty or equal None!'.format(sql))
189 
190 def delete(conn, sql, data):
191     '''删除数据'''
192     if sql is not None and sql != '':
193         if data is not None:
194             cu = get_cursor(conn)
195             for d in data:
196                 if SHOW_SQL:
197                     print('执行sql:[{}],参数:[{}]'.format(sql, d))
198                 cu.execute(sql, d)
199                 conn.commit()
200             close_all(conn, cu)
201     else:
202         print('the [{}] is empty or equal None!'.format(sql))
203 ###############################################################
204 ####            数据库操作CRUD     END
205 ###############################################################
206 
207 
208 ###############################################################
209 ####            测试操作     START
210 ###############################################################
211 def drop_table_test():
212     '''删除数据库表测试'''
213     print('删除数据库表测试...')
214     conn = get_conn(DB_FILE_PATH)
215     drop_table(conn, TABLE_NAME)
216 
217 def create_table_test():
218     '''创建数据库表测试'''
219     print('创建数据库表测试...')
220     create_table_sql = '''CREATE TABLE `student` (
221                           `id` int(11) NOT NULL,
222                           `name` varchar(20) NOT NULL,
223                           `gender` varchar(4) DEFAULT NULL,
224                           `age` int(11) DEFAULT NULL,
225                           `address` varchar(200) DEFAULT NULL,
226                           `phone` varchar(20) DEFAULT NULL,
227                            PRIMARY KEY (`id`)
228                         )'''
229     conn = get_conn(DB_FILE_PATH)
230     create_table(conn, create_table_sql)
231 
232 def save_test():
233     '''保存数据测试...'''
234     print('保存数据测试...')
235     save_sql = '''INSERT INTO student values (?, ?, ?, ?, ?, ?)'''
236     data = [(1, 'Hongten', '男', 20, '广东省广州市', '13423****62'),
237             (2, 'Tom', '男', 22, '美国旧金山', '15423****63'),
238             (3, 'Jake', '女', 18, '广东省广州市', '18823****87'),
239             (4, 'Cate', '女', 21, '广东省广州市', '14323****32')]
240     conn = get_conn(DB_FILE_PATH)
241     save(conn, save_sql, data)
242 
243 def fetchall_test():
244     '''查询所有数据...'''
245     print('查询所有数据...')
246     fetchall_sql = '''SELECT * FROM student'''
247     conn = get_conn(DB_FILE_PATH)
248     fetchall(conn, fetchall_sql)
249 
250 def fetchone_test():
251     '''查询一条数据...'''
252     print('查询一条数据...')
253     fetchone_sql = 'SELECT * FROM student WHERE ID = ? '
254     data = 1
255     conn = get_conn(DB_FILE_PATH)
256     fetchone(conn, fetchone_sql, data)
257 
258 def update_test():
259     '''更新数据...'''
260     print('更新数据...')
261     update_sql = 'UPDATE student SET name = ? WHERE ID = ? '
262     data = [('HongtenAA', 1),
263             ('HongtenBB', 2),
264             ('HongtenCC', 3),
265             ('HongtenDD', 4)]
266     conn = get_conn(DB_FILE_PATH)
267     update(conn, update_sql, data)
268 
269 def delete_test():
270     '''删除数据...'''
271     print('删除数据...')
272     delete_sql = 'DELETE FROM student WHERE NAME = ? AND ID = ? '
273     data = [('HongtenAA', 1),
274             ('HongtenCC', 3)]
275     conn = get_conn(DB_FILE_PATH)
276     delete(conn, delete_sql, data)
277 
278 ###############################################################
279 ####            测试操作     END
280 ###############################################################
281 
282 def init():
283     '''初始化方法'''
284     #数据库文件绝句路径
285     global DB_FILE_PATH
286     DB_FILE_PATH = 'c:\\test\\hongten.db'
287     #数据库表名称
288     global TABLE_NAME
289     TABLE_NAME = 'student'
290     #是否打印sql
291     global SHOW_SQL
292     SHOW_SQL = True
293     print('show_sql : {}'.format(SHOW_SQL))
294     #如果存在数据库表，则删除表
295     drop_table_test()
296     #创建数据库表student
297     create_table_test()
298     #向数据库表中插入数据
299     save_test()
300     
301 
302 def main():
303     init()
304     fetchall_test()
305     print('#' * 50)
306     fetchone_test()
307     print('#' * 50)
308     update_test()
309     fetchall_test()
310     print('#' * 50)
311     delete_test()
312     fetchall_test()
313 
314 if __name__ == '__main__':
315     main()