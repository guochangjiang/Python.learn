# coding: utf-8
from flask_wtf import Form
from wtforms import StringField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Optional


class WorkReviewForm(Form):
    """Form for add and edit work review"""
    title = StringField('标题', [Optional()], description='选填')
    content = TextAreaField('内容', [DataRequired("内容不能为空")])


class WorkReviewCommentForm(Form):
    """Form for add comment to work review"""
    content = TextAreaField('回复', [DataRequired("回复不能为空")])


class WorkImageForm(Form):
    """Form for add and edit work image"""
    image = HiddenField('图片', validators=[DataRequired('请上传图片后提交')])
    is_original = StringField('类别', validators=[DataRequired('请选择是否为原创作品')])
    from_url = StringField('来源', description='图片的来源网址，选填')
