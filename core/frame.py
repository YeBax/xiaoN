import jieba


class Frame:
    """
    对话框架类

    框架状态码
        0 等待询问问题
        1 等待分类结果
        2 等待标问准确结果

    """
    def __init__(self, user_id, create_time):
        self.user_id = user_id
        self.talk_list = []
        self.create_time = create_time
        self.redis_key = None
        self.frame_tag = None
        self.frame_type = 0     # 类型 0-询问 1-指令
        self.frame_state_code = 0
        self.frame_wait_next_talk_state = False

    def run(self):
        pass

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



