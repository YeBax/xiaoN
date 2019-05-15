# -*- coding: utf-8 -*-
import jieba
import uuid
from words import STOP_WORDS_LIST, YES_WORDS_LIST, NO_WORDS_LIST

__author__ = "Yebax"


class Talk:
    def __init__(self, user_id, talk_msg):
        """
        独立对话 初始化，
        talk类只处理句子
        与上下文无关，对话逻辑在frame类中体现
        """
        self.user_id = user_id  # 用户ID
        self.msg_id = None  # 消息ID
        self.talk_msg = talk_msg    # 消息内容，对话句子
        self.words_list = []    # 分词列表
        self.keywords_list = []     # 分词过滤后的，关键词列表

        self.__run()

    def get_msg_id(self):
        """
        根据 用户ID 使用UUID3 生成 消息ID
        :return: msg_id (消息ID)
        """
        self.msg_id = uuid.uuid3(uuid.NAMESPACE_URL, self.user_id)
        return self.msg_id

    def get_keywords_list(self):
        return self.keywords_list

    def yes_or_no_words(self):
        """
        判断 句子中 对错的词
        :return:
        """
        yes_words_number = 0
        no_words_number = 0

        for word in self.words_list:
            if word in YES_WORDS_LIST:
                yes_words_number += 1
            elif word in NO_WORDS_LIST:
                no_words_number += 1

        iscode = 0  # 相等 或者 都为0 不确定 对 还是 错 返回0
        if yes_words_number > no_words_number:
            iscode = 1  # 1 是
        elif yes_words_number < no_words_number:
            iscode = 2  # 2 不是

        return iscode

    def __run(self):
        self.__talk_to_words()
        self.__stop_words()

    def __talk_to_words(self):
        """
        分词列表
        :return:
        """
        self.words_list = jieba.cut(self.talk_msg.strip(), cut_all=True, HMM=True)
        self.words_list = list(self.words_list)
        print("分词结果：", self.words_list)

    def __stop_words(self):
        """
        去除 停用词，重复词，1个单字
        提取出 关键词语
        :return: 关键词列表
        """
        self.keywords_list = list(set([i for i in self.words_list if i not in STOP_WORDS_LIST or len(i) > 2]))
        print("关键词：", self.keywords_list)

    def sentiment_classify(self):
        """
        情感倾向分析
        自动对包含主观信息的文本进行情感倾向性判断（积极、消极、中性），并给出相应的置信度。
        为口碑分析、话题监控、舆情分析等应用提供基础技术支持，同时支持用户自行定制模型效果调优。
        :return:
        """
        pass

    def emotion(self):
        """
        对话情绪识别
        针对用户日常沟通文本背后所蕴含情绪的一种直观检测，可自动识别出当前会话者所表现出的一级和二级细分情绪类别及其置信度，
        针对正面和负面的情绪，还可给出参考回复话术。帮助企业更全面地把握产品服务质量、监控客户服务质量。
        在自动监控中如果发现有负面情绪出现，可以及时介入人工处理，帮助在有限的人工客服条件下，降低客户流失。
        :return:
        """
        pass


class Questions:
    def __init__(self, questions_id, question_name):
        self.question_id = questions_id
        self.question_name = question_name
        self.keywords_list = []

        self._run()

    def _run(self):
        words_list = jieba.cut(self.question_name, cut_all=True, HMM=True)
        self.keywords_list = list(set([i for i in words_list if i not in STOP_WORDS_LIST or len(i) > 2]))

    def get_keywords_list(self):
        return self.keywords_list

    def get_question_id(self):
        return self.question_id

    def get_question_name(self):
        return self.question_name


class Tags:
    def __init__(self, tag_id, tag_name, tag_belong_id):
        self.tag_id = tag_id    # 标签ID
        self.tag_name = tag_name    # 标签名称
        self.tag_belong_id = tag_belong_id      # 上级标签名称

    def get_tag_id(self):
        return self.tag_id

    def get_tag_name(self):
        return self.tag_name

    def get_tag_belong_id(self):
        return self.tag_belong_id



