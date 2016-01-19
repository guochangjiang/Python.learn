# coding: utf-8
from flask_wtf import Form
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Optional


class CollectionForm(Form):
    name = StringField('名称', validators=[DataRequired('集合名称不能为空')])
    full_name = StringField('全称', validators=[Optional()])
    # abbr = StringField('缩写', validators=[DataRequired('缩写不能为空')])
    desc = TextAreaField('简介', validators=[Optional()])
    cover = StringField('封面', validators=[Optional()])
    link = StringField('链接', validators=[Optional()])
    kind_id = SelectField('类别', [DataRequired('类别不能为空')], coerce=int)

    # 繁体
    name_tr = StringField('名称')
    full_name_tr = StringField('全称')
    desc_tr = TextAreaField('简介')
