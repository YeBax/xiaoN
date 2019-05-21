# -*- coding: utf-8 -*-
import pymysql
import redis
from setting import MYSQL_INFO, REDIS_INFO


mysql_conn = pymysql.connect(**MYSQL_INFO)

__author__ = "Yebax"


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


def mysql_query_where_equal(sql, s):
    """
    查询符合条件的数据
    :param sql:  查询语句
    :param s: 数值
    :return: 查询数据
    """
    try:
        cursor = mysql_conn.cursor()
        cursor.execute(sql, s)
        results = cursor.fetchall()
        cursor.close()
        return results
    except Exception as e:
        print(e)


def mysql_insert(sql, s):
    # 数据库写入
    cursor = mysql_conn.cursor()
    try:
        cursor.execute(sql, s)
        cursor.close()
        mysql_conn.commit()
    except Exception as e:
        print(e)
        cursor.close()
        mysql_conn.rollback()


def redis_get_frames():
    pass

