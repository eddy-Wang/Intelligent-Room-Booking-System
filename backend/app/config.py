

class Config:
    # 163 mail config
    DEBUG = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'rf_diicsu_rb@163.com'
    MAIL_PASSWORD = 'VAY5wcSNdMhDkZQv'
    MAIL_DEFAULT_SENDER = 'rf_diicsu_rb@163.com'

    # database config
    DB_HOST = 'diidrbs.mysql.polardb.rds.aliyuncs.com'
    DB_PORT = 3306
    DB_USER = 'administrator'
    DB_PASSWORD = '!admin123'
    DB_NAME = 'diidrbs'
