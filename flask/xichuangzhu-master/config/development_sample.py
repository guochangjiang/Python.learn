# coding: utf-8
from .default import Config


class DevelopmentConfig(Config):
    # App config
    DEBUG = True

    # Uploadsets config
    UPLOADS_DEFAULT_DEST = "/var/www/xcz_uploads"  # 上传文件存储路径
    UPLOADS_DEFAULT_URL = "http://localhost/xcz_uploads/"  # 上传文件访问URL

    SENTRY_DSN = ''

    MAIL_SERVER = ''
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_DEBUG = DEBUG
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    MAIL_DEFAULT_SENDER = ''
    MAIL_MAX_EMAILS = None
    MAIL_ADMIN_ADDR = ''

    # Db config
    SQLALCHEMY_DATABASE_URI = "mysql://root:password@localhost/xcz"

    HOST_STRING = ""

    # Aliyun OSS config
    OSS_HOST = 'oss.aliyuncs.com'
    OSS_KEY = ''
    OSS_SECRET = ''
    OSS_URL = ''
