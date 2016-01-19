# coding: utf-8
from flask_wtf import Form
from wtforms import StringField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired


class TopicForm(Form):
    """Form for add and edit topic"""
    title = StringField('标题', [DataRequired(message="标题不能为空")])
    content = TextAreaField('内容', [DataRequired(message="内容不能为空")])


class TopicCommentForm(Form):
    """Form for add comment to topic"""
    content = TextAreaField('回复', [DataRequired(message="回复不能为空")])