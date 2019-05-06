import jieba
import uuid
from words import STOP_WORDS_LIST, YES_WORDS_LIST, NO_WORDS_LIST


class Talk:
    def __init__(self, user_id, talk_msg, talk_time):
        """
        独立对话 初始化，
        talk类只处理句子
        与上下文无关，对话逻辑在frame类中体现
        """
        self.user_id = user_id
        self.msg_id = None
        self.talk_msg = talk_msg
        self.talk_time = talk_time
        self.words_list = []
        self.keywords_list = []

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

    def __run(self):
        self.__talk_to_words()
        self.__stop_words()

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


class Questions:
    def __init__(self, questions_list):
        self.questions_list = questions_list
        self.questions_dict = {}

    def get_questions_dict(self):
        for talks in self.questions_list:
            words_list = jieba.cut(talks.strip(), cut_all=True, HMM=True)
            keywords_list = list(set([i for i in words_list if i not in STOP_WORDS_LIST or len(i) > 2]))
            if talks in self.questions_dict:
                continue
            self.questions_dict[talks] = keywords_list

        return self.questions_dict




