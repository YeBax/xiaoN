import os
import sys

__author__ = "Yebax"

# 项目内部构建路径
# 例如这样格式: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# ----------------------------------------------------------------------
# 词库路径
DATA_PATH = os.path.join(BASE_DIR, 'data')
STOP_WORDS_PATH = os.path.join(DATA_PATH, 'stop_words.txt')
YES_WORDS_PATH = os.path.join(DATA_PATH, 'yes_words.txt')
NO_WORDS_PATH = os.path.join(DATA_PATH, 'no_words.txt')

# ----------------------------------------------------------------------
# data base info
MYSQL_INFO = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "123456",
    "database": "watchn",
    "charset": "utf8"
}

REDIS_INFO = {

}

# SQL
SQL_GET_TAGS_ID = """SELECT tag_id FROM corpus_keyword a LEFT JOIN corpus_word2tag b ON a.id=b.word_id WHERE a.word IN (%s);"""
SQL_GET_TAGS = """SELECT * FROM corpus_tag WHERE id IN (%s);"""
SQL_GET_TAGS_ALL = """SELECT * FROM corpus_tag;"""
SQL_GET_QUESTIONS_FOR_TAGS_ID = """SELECT q.id, q.question FROM (SELECT * FROM corpus_tag2question WHERE tag_id = %s) t LEFT JOIN corpus_queandans q ON t.question_id = q.id;"""
SQL_GET_ANSWER = """SELECT answer FROM corpus_queandans  WHERE id = %s;"""
SQL_ADD_QUESTIONS = """INSERT INTO corpus_collection(questions,create_time,state) VALUES(%s,NOW(),0);"""
SQL_QUERY_QUESTIONS = """SELECT * FROM corpus_collection WHERE questions IN (%s);"""

