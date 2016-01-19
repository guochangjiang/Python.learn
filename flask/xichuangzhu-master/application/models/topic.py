# coding: utf-8
import datetime
from ._base import db


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    click_num = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('topics', lazy='dynamic',
                                                      order_by="desc(Topic.create_time)"))

    def __repr__(self):
        return '<Topic %s>' % self.title


class TopicComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), primary_key=True)
    topic = db.relationship('Topic', backref=db.backref('comments', lazy='dynamic',
                                                        order_by="asc(TopicComment.create_time)"))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user = db.relationship('User', backref=db.backref('topic_comments', lazy='dynamic',
                                                      order_by="desc(TopicComment.create_time)"))

    def __repr__(self):
        return '<TopicComment %s>' % self.content