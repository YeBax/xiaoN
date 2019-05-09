from collections import Counter

from talk import Talk
from database import mysql_query_wherein, mysql_query_all
from setting import SQL_GET_TAGS, SQL_GET_TAGS_ID, SQL_GET_TAGS_ALL


class Frame:
    """
    对话框架类

    框架状态码  self.frame_state_code
        0 -> 1  初次询问 问题
        1 -> 2  检索分类，等待答复
        2 -> 3  肯定答复，匹配标准问题
        2 -> 4  否定答复，重新寻找分类
        4 -> 2  检索分类，等待答复
        2 -> -1 放弃询问，结束
        3 -> 5  返回标准问题，和答案
        5 -> -1 肯定答案，结束，记录一次 有效解决
        5 -> 6  否定答案，返回一次相似问题列表
        6 -> 7  选中列表中的问题，返回答案
        7 -> -1 肯定答案，结束，记录一次 有效解决
        6 -> -1 列表中无合适的问题，结束，记录一次 无效解决

    """

    process_dict = {
        0: "tags_process",
    }

    def __init__(self, user_id, create_time, frame_type=0):
        self.user_id = user_id
        self.talk_list = []
        self.response_words_list = []
        self.create_time = create_time
        self.update_time = None
        self.redis_key = None
        self.frame_tag = []
        self.frame_type = frame_type     # 类型 0-询问 1-指令
        self.frame_state_code = 0
        self.frame_wait_next_talk_state = False
        self.error_number = 0

    def receive_talk(self, talk_msg, talk_time):
        word = self.empty_repeat_words(talk_msg)
        if word != 0:
            return word
        self.update_time = talk_time

    def tags_process(self, talk_msg):
        """
        获得分类名称流程
        :param talk_msg:
        :return: 返回字符串，对话内容
        """
        response_word = ""
        code = self._get_tags(talk_msg)
        if code == 0:
            pass
        tags_name = self.frame_tag[0]

        return response_word

    def _get_tags(self, talk_msg):
        """
        获得分类名称，并放入 self.frame_tag 列表里
        :param talk_msg: 句子
        :return:  执行状态码
        """
        t = Talk(self.user_id, talk_msg)
        key_words_list = t.get_keywords_list()
        results_tags_id_tuple = mysql_query_wherein(SQL_GET_TAGS_ID, key_words_list)  # 从数据库 查找 关键词，获得 tags_id的列表

        if len(results_tags_id_tuple) == 0:
            return 0    # self.frame_tag 列表 没有数据

        tags_id_list = []
        for result in results_tags_id_tuple:
            tags_id_list.append(result[0])

        results_tags_tuple = mysql_query_wherein(SQL_GET_TAGS, tags_id_list)     # 根据tags_id的列表，获得tags

        tags_weight_dict = self.__tags_weight(tags_id_list)     # 计算权重

        for k in tags_weight_dict.keys():
            for result in results_tags_tuple:
                if result[0] == k:
                    self.frame_tag.append(result[1])
                    results_tags_tuple.remove(result)    # 找到了tags,就从results_tags_tuple中删除，提高效率，下次循环少一个
                    break   # 找到就退出循环，进行下一个

        return 1    # self.frame_tag 列表 有数据

    def update_state_code(self, state_code):
        """
        更改 对话框架 状态码
        :return:
        """
        self.frame_state_code = state_code
        self.error_number = 0

    def empty_repeat_words(self, talk_msg):
        """
        处理重复的消息 和 重复发送的消息
        :param
        :return:
        """
        if talk_msg.strip() == "":
            self.error_number += 1
            return '你好像什么都没输入，小N不知道你在问什么？'
        if talk_msg in self.talk_list:
            self.error_number += 1
            return "呀，你刚刚上句就这样说的，同学，你失忆了吗？"
        if talk_msg.strip() is self.talk_list[-1].strip():
            self.error_number += 1
            return "啊？你是不是发重复了？"
        return 0

    def __wait_response_for_tags(self):
        pass

    def __wait_timeout(self):
        """
        等待超时 做出处理，状态改为 -1 结束
        :return:
        """
        pass

    def get_answer(self):
        pass



    def add_talks(self, talk):
        self.talk_list.append(talk)

    def set_redis_key(self, key):
        self.redis_key = key

    def __query_db(self, words_list):
        pass

    def __insert_db(self):

        pass

    def __tags_weight(self, weight_list):
        """
        分类 权重
        目前简单的算了一下，权重肯定不准确
        :return: 权重字典
        """
        return Counter(weight_list)

    def questions_weight(self):
        """
        标准问题 权重
        :return:
        """
        pass

    def instructions(self):
        pass

    def collect_questions(self):
        """
        收集问题
        将问题 写入数据库
        更改frame的状态
        """
        return '~小N~未能帮你解决问题，已经将你的问题收集，之后会有更好的解答，感谢你为~小N~的数据训练做出贡献！加油哦！'
