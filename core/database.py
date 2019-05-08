import pymysql
import redis
from setting import MYSQL_INFO, REDIS_INFO

# test
from setting import SQL_GET_TAGS, SQL_GET_TAGS_ALL, SQL_GET_TAGS_ID

mysql_conn = pymysql.connect(**MYSQL_INFO)


def mysql_query_wherein(sql, args):
    # 查询 格式where in
    try:
        cursor = mysql_conn.cursor()
        in_p = ', '.join(list(map(lambda x: "'%s'" % x, args)))
        sql = sql % in_p
        print(sql)
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        return results
    except Exception as e:
        print(e)
        return []


def mysql_query_all(sql):
    # 查询全部数据
    try:
        cursor = mysql_conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        return results
    except Exception as e:
        print(e)


def mysql_insert(sql):
    # 数据库写入
    cursor = mysql_conn.cursor()
    try:
        cursor.execute(sql)
        cursor.close()
        mysql_conn.commit()
    except Exception as e:
        print(e)
        cursor.close()
        mysql_conn.rollback()



def mysql_get_questions():
    pass


def redis_get_frames():
    pass

# ---------------------------test---------------------------
# t = mysql_query_all(SQL_GET_TAGS_ALL)
# print(t)
t1 = mysql_query_wherein(SQL_GET_TAGS_ID, ["哈哈"])
t2 = mysql_query_wherein(SQL_GET_TAGS, [2,3,5])
# print(t1,len(t1))
for x in t1:
    print(x[0], type(x[0]))
