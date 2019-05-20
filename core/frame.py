# -*- coding: utf-8 -*-
import uuid
import time
from collections import Counter

from talk import Talk, Tags, Questions
from database import mysql_query_wherein, mysql_query_where_equal, mysql_insert
from setting import SQL_GET_TAGS, SQL_GET_TAGS_ID, SQL_GET_QUESTIONS_FOR_TAGS_ID, SQL_GET_ANSWER, SQL_ADD_QUESTIONS

__author__ = "Yebax"


class Frame:
    """
    对话框架类

    框架状态码  self.frame_state_code
        0   创建对话框架
        ----------------------------------------------
        1   问题
        2   指令
        -1  超时关闭对话，超过300秒，无再次接收消息
        ----------------------------------------------
        问题
        10  等待接收
                已经接收问题     ->  11
                超时             -> -1
        11  匹配分类
                匹配到分类   ->  13
                匹配分类权重小于0.5 ->12
                未找出分类  ->  10
        12  询问分类
                有效分类（列表中存在的分类） -> 13
                无效分类（不在列表中） -> 12
                多次无效    -> 10
        13  匹配答案
                匹配到答案  ->  10
                未匹配到答案 -> 10

        ============================== 之后再写 ==============================
        14  反馈
                解决问题
                未解决问题

        ----------------------------------------------
        指令
            20  等待指令

    """

    def __init__(self, user_id, create_time):
        self.user_id = str(user_id)
        self.talk_list = []     # 收到对话列表
        self.create_time = create_time
        self.update_time = None
        self.redis_key = None
        self.frame_tag = None
        self.tags_list = []
        # self.frame_type = 1     # 类型 1-询问 2-指令
        self.frame_state_code = 0   # 框架状态码，初始 0
        self.error_number = 0
        self.tags_weight_dict = {}  # 标签权重字典
        self.questions_weight_dict = {}     # 匹配问题权重字典
        self.frame_wait_next_talk_state = None     # 框架等待回答状态
        self.questions_words_last = None    # 上一个有效问题

        self.__set_redis_key()

        self.frame_state_code = 10  # 等待接收问题

    def receive_talk(self, talk_msg, talk_time):
        self.frame_wait_next_talk_state = False
        self.update_time = talk_time
        word = self._check_words(talk_msg)
        if word != 0:
            return word
        self.talk_list.append(talk_msg)

        while not self.frame_wait_next_talk_state:
            word = self.process_dict(self.frame_state_code)(talk_msg)

        return word

    def get_redis_key(self):
        return self.redis_key

    def process_dict(self, code):
        p_d = {
            10: self._tags_process,
            12: self._check_tags_process,
            13: self._response_answer_process,
            14: self._check_questions_process,

        }
        return p_d.get(code)

    # 私有函数
    # ====================================================================================================
    # 流程 process 函数

    def _tags_process(self, talk_msg):
        """
        获得分类名称流程
        :param talk_msg: 问题句子
        :return: 返回字符串，对话内容
        """
        code = self.__get_tags(talk_msg)
        # self.__update_state_code(11)
        print("获取分类状态码：", code)
        if not code:
            self.frame_wait_next_talk_state = True
            self.__update_state_code(10)    # 重新进入等待问题状态
            return "哎呀，小N同学，没有理解你在问什么，抱歉了！换一种问法试试吧。"

        self.questions_words_last = talk_msg    # 获得有效问题
        tags_id_list = list(self.tags_weight_dict.keys())
        results_tags_tuple = mysql_query_wherein(SQL_GET_TAGS, tags_id_list)  # 从数据库中，根据tags_id，获得tags

        if code == 1:
            tag_id = max(self.tags_weight_dict, key=self.tags_weight_dict.get)
            for result in results_tags_tuple:
                if result[0] == tag_id:
                    self.frame_tag = Tags(result[0], result[1], result[2])
                    print("匹配到大于0.5权重的分类，并创建分类: tag_id:%s, tag_name:%s, tag_belong_id:%s"
                          % (result[0], result[1], result[2]))
                    break
            self.__update_state_code(13)    # 即将开始匹配答案状态
            return

        # 匹配分类的权重小于0.5，进行询问分类
        tags_name_list = []
        for result in results_tags_tuple:
            tags_name_list.append(result[1])
            self.tags_list.append(Tags(result[0], result[1], result[2]))
        in_p = '\n'.join(list(map(lambda x: "'%s:【%s】'" % (x[0], x[1]), enumerate(tags_name_list, 1))))
        self.__update_state_code(12)    # 询问分类，等待分类名称状态
        self.frame_wait_next_talk_state = True
        return "小N已经找出关于问题的分类，那个是你想问题的呢？\n %s" % in_p

    def _check_tags_process(self, talk_msg):
        """
        检查用户反馈的分类名称
        句子中是否有分类名称，没有或者返回多个分类名称，再次询问
        :param talk_msg:
        :return:
        """
        talk = Talk(talk_msg)
        keywords_list = talk.get_keywords_list()
        tags_list = []
        for tags in self.tags_list:
            if tags.get_tag_name() in keywords_list:
                tags_list.append(tags)

        # 未匹配到分类，不更改 框架状态 保持 12
        if len(tags_list) == 1:
            self.frame_tag = tags_list[0]
            self.__update_state_code(13)    # 即将开始匹配答案状态
            return
        elif len(tags_list) > 1:
            self.frame_wait_next_talk_state = True
            return "你好像说了好几个分类的名称哦！"
        else:
            self.error_number += 1
            self.frame_wait_next_talk_state = True
            return "~小N~，没有明白你在说什么？"

    def _response_answer_process(self, talk_msg):
        """
        匹配答案
        :param talk_msg:
        :return:
        """
        talk = Talk(self.questions_words_last)
        results_questions_tuple = mysql_query_where_equal(SQL_GET_QUESTIONS_FOR_TAGS_ID, self.frame_tag.get_tag_id())  # 查询符合的问题
        if len(results_questions_tuple) == 0:
            return self.__collect_questions(talk)

        questions_list = []
        for result in results_questions_tuple:
            q = Questions(result[0], result[1])
            if q.get_keywords_list():   # 问题的关键词列表不为空时 有效，防止垃圾数据的影响
                questions_list.append(q)
        if not questions_list:  # 防止 问题列表 为空
            return self.__collect_questions(talk)

        self.questions_weight_dict = self.__questions_weight(questions_list, talk)  # 获取问题权重
        question_name = max(self.questions_weight_dict, key=self.questions_weight_dict.get)     # 获取最大值

        if not self.questions_weight_dict:
            return self.__collect_questions(talk)

        for question in questions_list:
            if question.get_question_name() == question_name:
                response_question = question
                response_answer = self.__get_answer(response_question)
                response_words = "太棒了~已经找到了你可能要想要的结果！\n 问题：【%s】\n 结果：%s"\
                                 % (response_question.get_question_name(), response_answer)
                self.__update_state_code(10)    # 重新进入等待问题
                return response_words

    def _check_questions_process(self, talk_msg):
        pass

    def _check_words(self, talk_msg):
        """
        处理重复的消息 和 重复发送的消息
        :param
        :return:
        """
        words = 0
        if talk_msg.strip() == "":
            self.error_number += 1
            words =  '嗨？你好像什么都没输入，~小N~不知道你在问什么？'
        if talk_msg in self.talk_list:
            self.error_number += 1
            words = "这句...~小N~觉得很眼熟！同学！！！你%s失忆了吗？" % ((self.error_number-1) * '真')
        if self.error_number > 5:
            words = "同学~小N~感觉你很无聊哦！"
        return words

    # ====================================================================================================
    # 私有基础函数方法

    def __get_tags(self, talk_msg):
        """
        从问题中，找出问题在那个分类中，找出返回1，没找出 返回 0
        :param talk_msg: 句子
        :return:  找到分类1 没找到分类 0
        """
        t = Talk(talk_msg)
        key_words_list = t.get_keywords_list()

        if not key_words_list:  # 没找到关键词
            return 0

        results_tags_id_tuple = mysql_query_wherein(SQL_GET_TAGS_ID, key_words_list)  # 从数据库 查找 关键词，获得 tags_id的列表
        if not results_tags_id_tuple:
            return 0    # 从关键词数据库中，未找到 tags_id的列表

        tags_id_list = []
        for result in results_tags_id_tuple:
            tags_id_list.append(result[0])

        self.tags_weight_dict = self.__tags_weight(key_words_list, tags_id_list)     # 计算标签权重
        if max(self.tags_weight_dict, key=self.tags_weight_dict.get) >= 0.5:
            return 1
        else:
            return 2

    def __update_state_code(self, state_code):
        """
        更改 对话框架 状态码
        :return:
        """
        self.frame_state_code = state_code
        self.error_number = 0   # 清除 错误积累次数

    def __wait_timeout(self):
        """
        等待超时 做出处理，状态改为 -1 结束
        :return:
        """
        pass

    def __get_answer(self, question):
        results = mysql_query_where_equal(SQL_GET_ANSWER, question.get_question_id())[0]
        return results[0]

    def __tags_weight(self, keys_words_list, tags_list):
        """
        分类 权重
        目前简单的算了一下，权重肯定不准确
        :return: 权重字典
        """
        words_num = len(keys_words_list)
        weight_dict = {}
        for k, v in Counter(tags_list).items():
            weight_dict[k] = v / words_num
        return weight_dict

    def __questions_weight(self, questions_list, talk):
        """
        标准问题 权重
        :return:
        """
        questions_weight_dict = {}
        talk_keywords_list = talk.get_keywords_list()
        talk_keywords_set = set(talk_keywords_list)
        for question in questions_list:
            question_keywords_list = question.get_keywords_list()
            question_keywords_set = set(question_keywords_list)
            intersection_words_list = talk_keywords_set.intersection(question_keywords_set)     # 交集词表
            intersection_count = len(intersection_words_list)  # 交集词频
            union_count = len(talk_keywords_set.union(question_keywords_set))   # 并集词频
            # difference_count = len(talk_keywords_set.difference(question_keywords_set))    # 差集词频

            if intersection_count == 0:     # 没有关键词
                continue

            weight = intersection_count / union_count
            intersection_probability = 1

            p1 = []
            p2 = []
            for word in intersection_words_list:
                p1.append(talk_keywords_list.index(word))
                p2.append(question_keywords_list.index(word))

            for i in range(intersection_count):
                for j in range(intersection_count):
                    if str(p1[i] < p1[j]) != str(p2[i] < p2[i]):
                        intersection_probability *= 1 / intersection_count

            weight = weight * 2 / 3 + intersection_probability * 1 / 3
            questions_weight_dict[question.get_question_name()] = weight
        return questions_weight_dict

    def __collect_questions(self, question):
        """
        收集问题
        将问题 写入数据库
        更改frame的状态
        """
        mysql_insert(SQL_ADD_QUESTIONS)     # 收集 未解决的问题
        self.__update_state_code(10)
        return '未能帮你解决问题，但已经记录下来了。~小N~知道了答案，就会立即就反馈给你哦！或者，换一种问法试试呢！'

    def __set_redis_key(self):
        """
        根据 用户ID 和 创建会话时间 UUID3 生成 redis_key
        :return:
        """
        self.redis_key = uuid.uuid3(uuid.NAMESPACE_DNS, str(self.user_id+self.create_time))






