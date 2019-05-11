# -*- coding: utf-8 -*-

__author__ = "Yebax"

from setting import SQL_GET_TAGS_ALL, SQL_GET_TAGS_ID, SQL_GET_TAGS, SQL_GET_ANSWER
from talk import Tags, Talk
from database import mysql_query_all, mysql_query_wherein, mysql_query_where_equal


tags_list = []

# tup = mysql_query_wherein(SQL_GET_TAGS, [2,4,6])
# for x in tup:
#     tag = Tags(x[0], x[1], x[2])
#     tags_list.append(tag)
#     print(tag.tag_id, tag.tag_name, tag.tag_belong_id)
#     print(tag.get_tag_id(), tag.get_tag_name(), tag.get_tag_belong_id())
#
#
# in_p = ', '.join(list(map(lambda x: "'%s'" % x.get_tag_name(), tags_list)))
# print(in_p)

#
# results = mysql_query_where_equal(SQL_GET_ANSWER, 1)[0]
# print(results[0])

l1 = ["a", "b", "c", "d"]
l2 = ["c", "e", "a"]
s1 = set(l1)
s2 = set(l2)
# c1 = len(s1.union(s2))
# c2 = len(s1.intersection(s2))

