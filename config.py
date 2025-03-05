# 配置信息
# 邮件服务器
# 数据库连接

import os


class Config:
    DEBUG = True
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.163.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 465))
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'rf_diicsu_rb@163.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'VAY5wcSNdMhDkZQv')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'rf_diicsu_rb@163.com')
