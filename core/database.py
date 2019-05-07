import pymysql
import redis
from setting import MYSQL_INFO, REDIS_INFO

mysql_conn = pymysql.connect(MYSQL_INFO)


def mysql_get_tags_id(args):
    try:
        cursor = mysql_conn.cursor()
        sql = """SELECT tag_id FROM corpus_keyword a LEFT JOIN corpus_word2tag b ON a.id=b.word_id 
                  WHERE a.word IN (%s);"""
        in_p = ', '.join(list(map(lambda x: "'%s'" % x, args)))
        sql = sql % in_p
        tag_id_list = cursor.execute(sql, args)
        cursor.close()
        return tag_id_list
    except Exception as e:
        print(e)


def mysql_get_tag(args):
    try:
        cursor = mysql_conn.cursor()
        sql = """select * from corpus_tag where id in (%s);"""
        in_p = ', '.join(list(map(lambda x: "'%s'" % x, args)))
        sql = sql % in_p
        tag_list = cursor.execute(sql, args)
        cursor.close()
        return tag_list
    except Exception as e:
        print(e)


def mysql_insert(sql):
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

