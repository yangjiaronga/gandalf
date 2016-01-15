WORK_DIR = '/tmp/repositories'
FLAKE8_EXECUTABLE = '/usr/local/bin/flake8'
HOST = '0.0.0.0'
PORT = 8080
DEBUG = False
REPORT_NO_MATCHING = False  # 没有在diff列表的文件的错误是否也报告
GITHUB_URL = 'http://github.com/'  # 行尾要加反斜杠
GITHUB_API_URL = 'https://api.github.com'  # 行尾不要加反斜杠
REPORT_CLOSEST = False # 错误出现在PR列出的文件中, 但是修改并不是此次PR中的diff里面是否报告
COMMENT_HEADER = ''


try:
    from local_settings import *
except ImportError:
    pass
