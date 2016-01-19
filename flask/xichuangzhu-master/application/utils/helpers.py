# coding: utf-8
import datetime
import uuid
from oss.oss_api import OssAPI
from flask import session, g, current_app, Response, json, url_for
from application.models import User
import functools


# count the time diff by timedelta, return a user-friendly format
def time_diff(time):
    """Friendly time gap"""
    now = datetime.datetime.now()
    delta = now - time
    if delta.days > 365:
        return '%d年前' % (delta.days / 365)
    if delta.days > 30:
        return '%d个月前' % (delta.days / 30)
    if delta.days > 0:
        return '%d天前' % delta.days
    if delta.seconds > 3600:
        return '%d小时前' % (delta.seconds / 3600)
    if delta.seconds > 60:
        return '%d分钟前' % (delta.seconds / 60)
    return '刚刚'


def check_is_me(user_id):
    """判断此user是否为当前在线的user"""
    return g.user and g.user.id == user_id


def signin_user(user, permenent):
    """Sign in user"""
    session.permanent = permenent
    session['user_id'] = user.id


def signout_user():
    """Sign out user"""
    session.pop('user_id', None)


def get_current_user():
    """获取当前user，同时进行session有效性的检测"""
    if not 'user_id' in session:
        return None
    user = User.query.filter(User.id == session['user_id']).first()
    if not user:
        signout_user()
        return None
    return user


def random_filename():
    """生成伪随机文件名"""
    return str(uuid.uuid4())


def save_to_oss(filename, uploadset):
    """将文件保存到OSS上，若保存失败，则抛出IO异常"""
    config = current_app.config
    oss = OssAPI(config.get('OSS_HOST'), config.get('OSS_KEY'), config.get('OSS_SECRET'))
    res = oss.put_object_from_file("xichuangzhu", filename,
                                   uploadset.config.destination + '/' + filename)
    if res.status != 200:
        raise IOError


def jsonify(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        r = func(*args, **kwargs)
        if isinstance(r, tuple):
            code, data = r
        else:
            code, data = 200, r
        response = Response(json.dumps(data), status=code, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    return wrapper


def absolute_url_for(endpoint, **values):
    """Absolute url for endpoint."""
    config = current_app.config
    site_domain = config.get('SITE_DOMAIN')
    relative_url = url_for(endpoint, **values)
    return join_url(site_domain, relative_url)


def join_url(pre_url, pro_url):
    """拼接url"""
    return "%s/%s" % (pre_url.rstrip('/'), pro_url.lstrip('/'))
