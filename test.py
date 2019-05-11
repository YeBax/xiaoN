# -*- coding: utf-8 -*-

__author__ = "Yebax"

from setting import SQL_GET_TAGS_ALL, SQL_GET_TAGS_ID, SQL_GET_TAGS
from talk import Tags, Talk
from database import mysql_query_all, mysql_query_wherein


tags_list = []

tup = mysql_query_wherein(SQL_GET_TAGS, [2,4,6])
for x in tup:
    tag = Tags(x[0], x[1], x[2])
    tags_list.append(tag)
    print(tag.tag_id, tag.tag_name, tag.tag_belong_id)
    print(tag.get_tag_id(), tag.get_tag_name(), tag.get_tag_belong_id())
print(tags_list)
