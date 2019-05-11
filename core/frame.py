import uuid
import time
from collections import Counter

from talk import Talk, Tags, Questions
from database import mysql_query_wherein, mysql_query_all, mysql_query_where_equal, mysql_insert
from setting import SQL_GET_TAGS, SQL_GET_TAGS_ID, SQL_GET_TAGS_ALL, SQL_GET_QUESTIONS_FOR_TAGS_ID, SQL_GET_ANSWER


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
        self.user_id = str(user_id)
        self.talk_list = []
        self.response_words_list = []
        self.create_time = create_time
        self.update_time = None
        self.redis_key = None
        self.frame_tags_list = []
        self.frame_type = frame_type     # 类型 0-询问 1-指令
        self.frame_state_code = 0
        self.frame_wait_next_talk_state = False
        self.error_number = 0
        self.tags_weight_dict = {}  # 标签权重字典
        self.questions_weight_dict = {}     # 匹配问题权重字典

        self.__set_redis_key()

    def receive_talk(self, talk_msg, talk_time):
        word = self.__empty_repeat_words(talk_msg)
        if word != 0:
            return word
        self.update_time = talk_time
        # self.__add_talks(talk_msg.strip())
        return "小N 为你服务！"

    def get_redis_key(self):
        return self.redis_key

    # 私有函数
    # ====================================================================================================
    # 流程 process 函数
    def _tags_process(self, talk_msg):
        """
        获得分类名称流程
        :param talk_msg: 问题句子
        :return: 返回字符串，对话内容
        """
        response_word = "小N，"
        code = self.__get_tags(talk_msg)
        if code == 0:
            tags_list = []
            results_tags_all_tuple = mysql_query_all(SQL_GET_TAGS_ALL)
            for result in results_tags_all_tuple:
                tags_list.append(result[1])
            in_p = ', '.join(list(map(lambda x: "'%s'" % x, tags_list)))
            response_word += "非常想解决你的问题，但还是不清楚你问哪个方面？\n请在以下选项中，选择一个分类吧：\n %s\n" % in_p
        else:
            tags_name = self.frame_tags_list[0].get_tag_name()
            response_word += "好像找到了，你的问题是关于【%s】方面的吗？\n" % tags_name
            if len(self.frame_tags_list[1:]) > 0:
                in_p = ', '.join(list(map(lambda x: "'%s'" % x.get_tag_name(), self.frame_tags_list[1:])))
                response_word += '要是我理解错了，那就从下面的选项中，选择一个分类吧！\n %s\n' % in_p

        self.__update_state_code(1)   # 状态设为 1  已经问过问题，进入等待回话分类的准确性的状态
        return response_word

    def _check_tags_process(self, talk_msg):
        """
        检查返回的话  确定词 or 否定词  or 标签名称
        :param talk_msg:
        :return:
        """
        response_word = "~小N~，"
        talk = Talk(self.user_id, talk_msg)
        keywords_list = talk.get_keywords_list()
        iscode = talk.yes_or_no_words()
        if len(self.frame_tags_list) == 0:
            results_tags_all_tuple = mysql_query_all(SQL_GET_TAGS_ALL)
            for result in results_tags_all_tuple:
                tag_name = result[1]
                if tag_name == talk_msg and tag_name in keywords_list:
                    tag = Tags(result[0], result[1], result[2])
                    self.frame_tags_list.append(tag)
                    response_word += self._response_answer_process(tag, talk)
                    break
        else:
            if iscode == 1:
                response_word += self._response_answer_process(self.frame_tags_list[0], talk)
            elif iscode == 2:
                in_p = ', '.join(list(map(lambda x: "'%s'" % x.get_tag_name(), self.frame_tags_list[1:])))
                response_word += "这个分类不对嘛？\n从下面选择一个你认为的分类吧！\n %s\n" % in_p
            elif iscode == 0:
                response_word += "没有明白你的意思，再说一次吧！"
            else:
                for tag in self.frame_tags_list:
                    tag_name = tag.get_tag_name()
                    if tag_name == talk_msg and tag_name in keywords_list:
                        self.frame_tags_list.remove(tag)    # 删除tag 对象
                        self.frame_tags_list.insert(0, tag)     # 将tag插入列表首位，保证self.frame_tags_list[0]为目标分类
                        response_word += self._response_answer_process(tag, talk)
                        break

        if response_word == "小N，":
            response_word += "不知道你在说什么，换个方式回答吧！"

        return response_word

    def _response_answer_process(self, tag, talk):
        results_questions_tuple = mysql_query_where_equal(SQL_GET_QUESTIONS_FOR_TAGS_ID, tag.get_tag_id())  # 查询符合的问题
        if results_questions_tuple.count() == 0:
            return self.__collect_questions(talk)

        questions_list = []
        for result in results_questions_tuple:
            q = Questions(result[0], result[1])
            if q.get_keywords_list():   # 问题的关键词列表不为空时 有效，防止垃圾数据的影响
                questions_list.append(q)
        if not questions_list:  # 防止 问题列表 为空
            return self.__collect_questions(talk)

        self.questions_weight_dict = self.__questions_weight(questions_list, talk)  # 获取问题权重
        response_question = max(self.questions_weight_dict, key=self.questions_weight_dict.get)     # 获取最大值
        response_answer = self.__get_answer(response_question)
        response_words = "太棒了~已经找到了你可能要想要的结果！\n 相似问题：【%s】\n 答案结果：%s" \
                         % (response_question.get_question_name(), response_answer)
        return response_words


    # ====================================================================================================
    # 私有基础函数方法

    def __get_tags(self, talk_msg):
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

        self.tags_weight_dict = self.__tags_weight(tags_id_list)     # 计算标签权重

        for k in self.tags_weight_dict.keys():
            for result in results_tags_tuple:
                if result[0] == k:
                    tag = Tags(result[0], result[1], result[2])
                    self.frame_tags_list.append(tag)    # self.frame_tags_list 存入标签（分类）对象
                    results_tags_tuple.remove(result)    # 找到了tags,就从results_tags_tuple中删除，提高效率，下次循环少一个
                    break   # 找到就退出循环，进行下一个

        return 1    # self.frame_tags_list 列表 有数据

    def __update_state_code(self, state_code):
        """
        更改 对话框架 状态码
        :return:
        """
        self.frame_state_code = state_code
        self.error_number = 0   # 清除 错误积累次数

    def __empty_repeat_words(self, talk_msg):
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
        if self.talk_list and talk_msg.strip() is self.talk_list[-1].key():
            self.error_number += 1
            return "啊？你是不是发重复了？"
        return 0

    def __wait_timeout(self):
        """
        等待超时 做出处理，状态改为 -1 结束
        :return:
        """
        pass

    def __get_answer(self, question):
        results = mysql_query_where_equal(SQL_GET_ANSWER, question.get_question_id())[0]
        return results[0]

    def __add_talks(self, question, answer):
        """
        添加一次对话内容
        :param question: 用户的问题
        :param answer: 机器人小N的回答
        :return:
        """
        self.talk_list.append({question: answer})

    def __tags_weight(self, weight_list):
        """
        分类 权重
        目前简单的算了一下，权重肯定不准确
        :return: 权重字典
        """
        return Counter(weight_list)

    def __questions_weight(self, questions_list, talk):
        """
        标准问题 权重
        :return:
        """
        questions_weight_dict = {}
        talk_keywords_list = talk.get_keywords_list()
        talk_keywords_set = set(talk_keywords_list)
        talk_keywords_count = len(talk_keywords_set)
        for question in questions_list:
            weight = 0
            question_keywords_list = question.get_keywords_list()
            question_keywords_set = set(question_keywords_list)
            questions_keywords_count = len(question_keywords_set)  # 问题关键词数量
            union_count = len(talk_keywords_set.union(question_keywords_set))   # 并集词频
            intersection_count = len(talk_keywords_set.intersection(question_keywords_set))     # 交集词频
            difference_count = len(talk_keywords_set.difference(question_keywords_set))    # 差集词频

            if intersection_count == 0:     # 没有关键词
                questions_weight_dict[question] = weight
                break

            if intersection_count / union_count == 1:   # 全部关键词相同
                weight = 1

            weight = intersection_count / union_count * \
                     min(intersection_count, difference_count) / max(intersection_count, difference_count)

            list_probability = 1 / intersection_count ** 2

            p1 = []
            p2 = []
            for word in talk_keywords_set.intersection(question_keywords_set):
                p1.append(talk_keywords_list.index(word))
                p2.append(question_keywords_list.index(word))

            for i in range(intersection_count):
                for j in range(i+1, intersection_count):
                    if p1[i] < p1[j] == p2[i] < p2[i]:
                        list_probability /= 1 - 1 / intersection_count
                list_probability /= 1 / intersection_count

            weight *= list_probability
            questions_weight_dict[question] = weight
        return questions_weight_dict

    def __collect_questions(self, question):
        """
        收集问题
        将问题 写入数据库
        更改frame的状态
        """

        return '未能帮你解决问题，已经将你的问题收集，之后会有更好的解答，感谢你为~小N~的数据训练做出贡献！加油哦！'

    def __set_redis_key(self):
        """
        根据 用户ID 和 创建会话时间 UUID3 生成 redis_key
        :return:
        """
        self.redis_key = uuid.uuid3(uuid.NAMESPACE_DNS, str(self.user_id+self.create_time))





