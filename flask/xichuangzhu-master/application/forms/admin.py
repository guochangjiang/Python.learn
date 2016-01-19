# coding: utf-8
from flask_wtf import Form
from wtforms import StringField, TextAreaField, SelectField, IntegerField, HiddenField
from wtforms.validators import DataRequired


class WorkForm(Form):
    """Form for add & edit work"""
    title = StringField('标题', [DataRequired('标题不能为空')])
    title_suffix = StringField('标题后缀')
    mobile_title = StringField('移动版标题')
    type_id = SelectField('类别', [DataRequired("类别不能为空")], coerce=int)
    layout = SelectField('布局', [DataRequired('布局不能为空')],
                         choices=[('center', '居中'), ('indent', '段落缩进')])
    author_id = SelectField('作者', [DataRequired('作者不能为空')], coerce=int)
    baidu_wiki = StringField('百度百科')
    foreword = TextAreaField('序')
    intro = TextAreaField('评析')
    content = TextAreaField('内容', [DataRequired('内容不能为空')])
    mobile_content = TextAreaField('移动版内容')

    # 繁体
    title_tr = StringField('标题')
    title_suffix_tr = StringField('标题后缀')
    foreword_tr = TextAreaField('序')
    content_tr = TextAreaField('内容')
    intro_tr = TextAreaField('评析')
    mobile_title_tr = StringField('移动版标题')
    mobile_content_tr = TextAreaField('移动版内容')


class AuthorForm(Form):
    """Form for add & edit author"""
    name = StringField('姓名', [DataRequired('姓名不能为空')])
    dynasty_id = SelectField('朝代', [DataRequired('朝代不能为空')], coerce=int)
    birth_year = StringField('生年', [DataRequired('生年不能为空')])
    death_year = StringField('卒年')
    baidu_wiki = StringField('百科')
    intro = TextAreaField('简介', [DataRequired('简介不能为空')])

    # 繁体
    name_tr = StringField('姓名')
    intro_tr = TextAreaField('简介')


class WorkQuoteForm(Form):
    """Form for add & edit quote for work"""
    quote = StringField('摘录', [DataRequired('摘录不能为空')])

    # 繁体
    quote_tr = StringField('摘录')


class DynastyForm(Form):
    """Form for add & edit dynasty"""
    name = StringField('朝代', [DataRequired('朝代不能为空')])
    intro = TextAreaField('简介', [DataRequired('简介不能为空')])
    start_year = IntegerField('起始年', [DataRequired('起始年不能为空')])
    end_year = IntegerField('结束年', [DataRequired('结束年不能为空')])

    # 繁体
    name_tr = StringField('朝代')
    intro_tr = TextAreaField('简介')
