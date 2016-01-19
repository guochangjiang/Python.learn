# coding: utf-8
import datetime
from ._base import db


class CollectWork(db.Model):
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user = db.relationship('User', backref=db.backref('collect_works', lazy='dynamic'))

    work_id = db.Column(db.Integer, db.ForeignKey('work.id'), primary_key=True)
    work = db.relationship('Work',
                           backref=db.backref('collectors', lazy='dynamic', cascade='delete'))

    def __repr__(self):
        return '<User %d collect Work %d>' % (self.user_id, self.work_id)


class CollectWorkImage(db.Model):
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user = db.relationship('User', backref=db.backref('collect_work_images', lazy='dynamic'))

    work_image_id = db.Column(db.Integer, db.ForeignKey('work_image.id'), primary_key=True)
    work_image = db.relationship('WorkImage',
                                 backref=db.backref('collectors', lazy='dynamic', cascade='delete'))

    def __repr__(self):
        return '<User %d collect WorkImage %d>' % (self.user_id, self.work_image_id)