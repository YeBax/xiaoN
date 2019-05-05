import os
import sys

# 项目内部构建路径
# 例如这样格式: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'core'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# ----------------------------------------------------------------------
# 词库路径
DATA_PATH = os.path.join(BASE_DIR, 'data')
STOP_WORDS_PATH = os.path.join(DATA_PATH, 'stop_words.txt')
YES_WORDS_PATH = os.path.join(DATA_PATH, 'yes_words.txt')
NO_WORDS_PATH = os.path.join(DATA_PATH, 'no_words.txt')

# ----------------------------------------------------------------------
