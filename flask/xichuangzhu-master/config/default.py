# coding: utf-8
import os


class Config(object):
    """配置基类"""
    # Flask app config
    DEBUG = False
    TESTING = False
    SECRET_KEY = "\xb5\xb3}#\xb7A\xcac\x9d0\xb6\x0f\x80z\x97\x00\x1e\xc0\xb8+\xe9)\xf0}"
    PERMANENT_SESSION_LIFETIME = 3600 * 24 * 7
    SESSION_COOKIE_NAME = 'xcz_session'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Root path of project
    PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Site domain
    SITE_DOMAIN = "http://localhost:5000"

    # SQLAlchemy config
    # See:
    # https://pythonhosted.org/Flask-SQLAlchemy/config.html#connection-uri-format
    # http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html#database-urls
    SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost/xcz"

    # SMTP config
    MAIL_SERVER = ''
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_DEBUG = DEBUG
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    MAIL_DEFAULT_SENDER = ''
    MAIL_MAX_EMAILS = None
    MAIL_ADMIN_ADDR = ''  # 管理员邮箱

    # UploadSets config
    UPLOADS_DEFAULT_DEST = "/var/www/xcz_uploads"  # 上传文件存储路径
    UPLOADS_DEFAULT_URL = "http://localhost/xcz_uploads/"  # 上传文件访问URL

    # Flask-DebugToolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # Sentry config
    SENTRY_DSN = ''

    # Host string, used by fabric
    HOST_STRING = ""

    # Douban OAuth2 config
    DOUBAN_CLIENT_ID = '0cf909cba46ce67526eb1d62ed46b35f'
    DOUBAN_SECRET = '4c87a8ef33e6c6be'
    DOUBAN_REDIRECT_URI = '%s/signin' % SITE_DOMAIN
    DOUBAN_LOGIN_URL = "https://www.douban.com/service/auth2/auth?client_id=%s&redirect_uri=%s" \
                       "&response_type=code" % (DOUBAN_CLIENT_ID, DOUBAN_REDIRECT_URI)

    # Aliyun OSS config
    OSS_HOST = 'oss.aliyuncs.com'
    OSS_KEY = ''
    OSS_SECRET = ''
    OSS_URL = ''
