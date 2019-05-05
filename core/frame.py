import jieba


class Frame:
    def __init__(self, user_id, create_time):
        self.user_id = user_id
        self.talk_list = []
        self.create_time = create_time
        self.redis_key = None
        self.frame_tag = None

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





