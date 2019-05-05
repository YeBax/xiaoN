import jieba
import time
import hashlib


class Talk:
    def __init__(self, user_id, talk_msg, talk_time):
        self.user_id = user_id
        self.msg_id = None
        self.talk_msg = talk_msg
        self.talk_time = talk_time
        self.word_list = []
        self.keyword_list = []

    def run(self):
        pass

    def init_msg_id(self):
        # 用户ID 和 时间 生成 消息ID
        pass

    def get_msg_id(self):
        pass

    def talk_to_word(self):
        # 返回 分词列表
        pass

    def __stop_word(self):
        # 去除停用词，重复词
        # 返回 关键词列表
        pass

