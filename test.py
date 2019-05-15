# -*- coding: utf-8 -*-

__author__ = "Yebax"

from setting import SQL_GET_TAGS_ALL, SQL_GET_TAGS_ID, SQL_GET_TAGS, SQL_GET_ANSWER
from talk import Tags, Talk
from database import mysql_query_all, mysql_query_wherein, mysql_query_where_equal
import math

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

l1 = ["a", "b", "c", "d", "e"]
l2 = ["a", "c", "b", "e"]
s1 = set(l1)
s2 = set(l2)
s3 = s1.intersection(s2)
# c1 = len(s1.union(s2))
# c2 = len(s1.intersection(s2))
s3_count = len(s3)
print(s3_count)

w = 1

p1 = []
p2 = []
for word in s3:
    p1.append(l1.index(word))
    p2.append(l2.index(word))
print(p1)
print(p2)

num = 0
int_x = math.ceil(math.sqrt(s3_count))
for i in range(s3_count):
    for j in range(s3_count):
        num += 1
        f1 = p1[i] < p1[j]
        f2 = p2[i] < p2[j]
        print(f1, f2)
        if str(f1) != str(f2):
            w *= 1 / s3_count

print(w)
print(num)





# import jieba
# talk_msg = "是吗"
# words_list = jieba.cut(talk_msg.strip(), cut_all=True, HMM=True)
# print(list(words_list))