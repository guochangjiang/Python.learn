# coding: utf-8
import datetime
from flask import current_app
from ._base import db


class Work(db.Model):
    """作品"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    title_suffix = db.Column(db.String(50))  # 完整的标题，用于没有题目的词，使用第一个短句作为其题目
    foreword = db.Column(db.Text())
    content = db.Column(db.Text())
    intro = db.Column(db.Text())
    baidu_wiki = db.Column(db.String(200))
    layout = db.Column(db.String(10))
    highlight = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now)
    highlight_at = db.Column(db.DateTime)

    mobile_title = db.Column(db.String(50))
    mobile_content = db.Column(db.Text())

    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship('Author', backref=db.backref('works', lazy='dynamic'))

    type_id = db.Column(db.Integer, db.ForeignKey('work_type.id'))
    type = db.relationship('WorkType', backref=db.backref('works', lazy='dynamic'))

    # 繁体
    title_tr = db.Column(db.String(50))
    title_suffix_tr = db.Column(db.String(50))
    foreword_tr = db.Column(db.Text())
    content_tr = db.Column(db.Text())
    intro_tr = db.Column(db.Text())
    mobile_title_tr = db.Column(db.String(50))
    mobile_content_tr = db.Column(db.Text())

    def populate_tr_fields(self):
        import opencc

        self.title_tr = opencc.convert(self.title or "", config='s2t.json')
        self.title_suffix_tr = opencc.convert(self.title_suffix or "", config='s2t.json')
        self.foreword_tr = opencc.convert(self.foreword or "", config='s2t.json')
        self.content_tr = opencc.convert(self.content or "", config='s2t.json')
        self.intro_tr = opencc.convert(self.intro or "", config='s2t.json')
        self.mobile_title_tr = opencc.convert(self.mobile_title or "", config='s2t.json')
        self.mobile_content_tr = opencc.convert(self.mobile_content or "", config='s2t.json')

    @property
    def full_title(self):
        if self.title_suffix and '·' not in self.title:
            return "%s · %s" % (self.title, self.title_suffix)
        else:
            return self.title

    def __repr__(self):
        return '<Work %s>' % self.title


class WorkType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    en = db.Column(db.String(50))
    cn = db.Column(db.String(50))

    # 繁体
    cn_tr = db.Column(db.String(50))

    def __repr__(self):
        return '<WorkType %s>' % self.cn


class WorkImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200))
    is_original = db.Column(db.Boolean, default=False)
    from_url = db.Column(db.String(250))
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)

    work_id = db.Column(db.Integer, db.ForeignKey('work.id'))
    work = db.relationship('Work', backref=db.backref('images', lazy='dynamic'))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('work_images', lazy='dynamic',
                                                      order_by="desc(WorkImage.create_time)"))

    @property
    def url(self):
        return current_app.config['OSS_URL'] + self.filename

    def __repr__(self):
        return '<WorkImage %s>' % self.filename


class WorkReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    is_publish = db.Column(db.Boolean)
    click_num = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)

    work_id = db.Column(db.Integer, db.ForeignKey('work.id'))
    work = db.relationship('Work', backref=db.backref('reviews', lazy='dynamic',
                                                      order_by="desc(WorkReview.create_time)"))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('work_reviews', lazy='dynamic',
                                                      order_by="desc(WorkReview.create_time)"))

    def __repr__(self):
        return '<WorkReview %s>' % self.title


class WorkReviewComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)

    review_id = db.Column(db.Integer, db.ForeignKey('work_review.id'), primary_key=True)
    review = db.relationship('WorkReview',
                             backref=db.backref('comments', lazy='dynamic',
                                                order_by="desc(WorkReviewComment.create_time)"))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user = db.relationship('User',
                           backref=db.backref('work_review_comments', lazy='dynamic',
                                              order_by="desc(WorkReviewComment.create_time)"))

    def __repr__(self):
        return '<WorkReviewComment %s>' % self.content
