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

l1 = ["a", "b", "c", "d",'e','k']
l2 = ["c", "b", "a", "e", 'k','d']
s1 = set(l1)
s2 = set(l2)
s3 = s1.intersection(s2)
# c1 = len(s1.union(s2))
# c2 = len(s1.intersection(s2))
# s3_count = len(s3)
s3_count = 3
w = 1 / s3_count ** 2
p1 = []
p2 = []
print(w)
for word in s3:
    p1.append(l1.index(word))
    p2.append(l2.index(word))
print(p1)
print(p2)

for i in range(s3_count-1):
    for j in range(i+1, s3_count):
        p1_code = 0
        p2_code = 0
        if p1[i] < p1[j]: p1_code = 1
        if p2[i] < p2[j]: p2_code = 1
        if not p1_code == p2_code:
            print(i,j)
            print("p1[i]",p1[i],"p1[j]",p1[j])
            print("p2[i]",p2[i],"p2[j]", p2[j])
            w /= 1 - 1 / s3_count
    print(i)
    w /= 1 / s3_count
print(w)