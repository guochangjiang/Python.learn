# coding: utf-8
import datetime
import re
import markdown2
from werkzeug.utils import escape
from flask import g
from application.models import CollectWork, CollectWorkImage


def timesince(value):
    """Friendly time gap"""
    now = datetime.datetime.now()

    if now < value:
        return "刚刚"

    delta = now - value
    if delta.days > 365:
        return '%d 年前' % (delta.days / 365)
    if delta.days > 30:
        return '%d 个月前' % (delta.days / 30)
    if delta.days > 0:
        return '%d 天前' % delta.days
    if delta.seconds > 3600:
        return '%d 小时前' % (delta.seconds / 3600)
    if delta.seconds > 60:
        return '%d 分钟前' % (delta.seconds / 60)
    return '刚刚'


def clean_work(content):
    """截取作品内容时，去除其中一些不需要的元素"""
    c = re.sub(r'<([^<]+)>', '', content)
    c = c.replace('%', '')
    c = c.replace('（一）', "")
    c = c.replace('(一)', "")
    return c


def markdown_work(content):
    """将作品内容格式化为HTML标签
    Add comment -> Split ci -> Generate paragraph
    """
    c = re.sub(r'<([^<]+)>', r"<sup title='\1'></sup>", content)
    c = c.replace('%', "&nbsp;&nbsp;&nbsp;&nbsp;")
    c = markdown2.markdown(c)
    return c


def markdown(content):
    """使用markdown处理字符串"""
    return markdown2.markdown(content)


def format_year(year):
    """将数字表示的年转换成中文"""
    return str(year).replace('-', '前') + "年"


def format_text(text):
    """将文本进行HTML转义，然后将换行符替换为div"""
    return escape(text).replace('\n', "<div class='text-gap'></div>")


def is_work_collected(work):
    """判断当前用户是否收藏此作品"""
    return g.user and CollectWork.query.filter(CollectWork.work_id == work.id).filter(
        CollectWork.user_id == g.user.id).count() > 0


def is_work_image_collected(work_image):
    """判断当前用户是否收藏此作品图片"""
    return g.user and CollectWorkImage.query.filter(CollectWorkImage.user_id == g.user.id).filter(
        CollectWorkImage.work_image_id == work_image.id).count() > 0
