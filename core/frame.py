from talk import Talk


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
    def __init__(self, user_id, create_time, frame_type=0):
        self.user_id = user_id
        self.talk_list = []
        self.create_time = create_time
        self.redis_key = None
        self.frame_tag = None
        self.frame_type = frame_type     # 类型 0-询问 1-指令
        self.frame_state_code = 0
        self.frame_wait_next_talk_state = False

    def receive_talk(self, talk_msg, talk_time):
        if talk_msg.strip() == "":
            return '你好像什么都没输入，小N不知道你在问什么啊？'
        if self.frame_state_code == 0:
            t = Talk(self.user_id, talk_msg, talk_time)
            t.get_keywords_list()

    def add_talks(self, talk):
        self.talk_list.append(talk)

    def set_redis_key(self, key):
        self.redis_key = key

    def __query_db(self):
        pass

    def __insert_db(self):

        pass

    def tags_weight(self):
        """
        分类 权重
        :return:
        """
        pass

    def questions_weight(self):
        """
        标准问题 权重
        :return:
        """
        pass

    def instructions(self):
        pass


