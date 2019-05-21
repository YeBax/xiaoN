from setting import STOP_WORDS_PATH, YES_WORDS_PATH, NO_WORDS_PATH


def file_to_list(path):
    with open(path, 'r', encoding='utf-8') as f:
        words = f.readlines()
    words_list = [i.strip() for i in words if i.strip() != '']
    return words_list

STOP_WORDS_LIST = file_to_list(STOP_WORDS_PATH)
YES_WORDS_LIST = file_to_list(YES_WORDS_PATH)
NO_WORDS_LIST = file_to_list(NO_WORDS_PATH)

