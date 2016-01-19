# coding: utf-8
from ._base import db


class Dynasty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    intro = db.Column(db.Text())
    start_year = db.Column(db.Integer)
    end_year = db.Column(db.Integer)

    # 繁体
    name_tr = db.Column(db.String(50))
    intro_tr = db.Column(db.Text())

    def populate_tr_fields(self):
        import opencc

        self.name_tr = opencc.convert(self.name or "", config='s2t.json')
        self.intro_tr = opencc.convert(self.intro or "", config='s2t.json')

    def __repr__(self):
        return '<Dynasty %s>' % self.name