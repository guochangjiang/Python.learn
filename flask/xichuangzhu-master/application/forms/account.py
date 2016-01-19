# coding: utf-8
from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email
from ..models import User


class SignupForm(Form):
    """Form for send email"""
    email = StringField('邮箱', [DataRequired(message="邮箱不能为空"), Email(message="无效的邮箱")],
                        description='你常用的邮箱')

    def validate_email(self, field):
        if User.query.filter(User.email == field.data).count() > 0:
            raise ValueError('邮箱已被使用')


class SettingsForm(Form):
    """Form for personal settings"""
    signature = TextAreaField('签名', [])
