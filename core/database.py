import pymysql
import redis
from setting import MYSQL_INFO, REDIS_INFO


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

