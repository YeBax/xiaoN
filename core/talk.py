import jieba
import uuid
from words import STOP_WORDS_LIST, YES_WORDS_LIST, NO_WORDS_LIST


class Talk:
    def __init__(self, user_id, talk_msg, talk_time, talk_type):
        """
        独立对话 初始化，
        talk类只处理句子
        与上下文无关，对话逻辑在frame类中体现
        """
        self.user_id = user_id
        self.msg_id = None
        self.talk_msg = talk_msg
        self.talk_time = talk_time
        self.talk_type = talk_type
        self.words_list = []
        self.keywords_list = []

    def run(self):
        pass

    def get_msg_id(self):
        """
        根据 用户ID 使用UUID3 生成 消息ID
        :return: msg_id (消息ID)
        """
        self.msg_id = uuid.uuid3(uuid.NAMESPACE_URL, self.user_id)
        return self.msg_id

    def __talk_to_words(self):
        """
        分词列表
        :return:
        """
        self.words_list = jieba.cut(self.talk_msg.strip(), cut_all=True, HMM=True)

    def __stop_words(self):
        """
        去除 停用词，重复词，1个单字
        提取出 关键词语
        :return: 关键词列表
        """
        self.keywords_list = list(set([i for i in self.words_list if i not in STOP_WORDS_LIST or len(i) > 2]))



