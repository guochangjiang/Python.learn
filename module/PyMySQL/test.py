import pymysql
conn = pymysql.connect(host='127.0.0.1', user='root', passwd="python123", db='mysql')
# conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd=None, db='mysql')

try:
    with conn.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `user` (`Host`, `User`, `Password`) VALUES (%s, %s, %s)"
        cursor.execute(sql, ('localhost', 'gcj', 'gcj123'))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    conn.commit()

    with conn.cursor() as cur:
        cur.execute("SELECT Host,User FROM user")
        # print cur.description
        # r = cur.fetchall()
        # print r
        # ...or...
        for r in cur:
            print(r)

finally:
    conn.close()