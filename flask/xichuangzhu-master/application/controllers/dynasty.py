# coding: utf-8
from flask import render_template, redirect, url_for, Blueprint
from ..models import db, Dynasty
from ..forms import DynastyForm
from application.utils.permissions import AdminPermission

bp = Blueprint('dynasty', __name__)


@bp.route('/dynasty/<int:uid>')
def view(uid):
    """朝代"""
    dynasties = Dynasty.query.order_by(Dynasty.start_year.asc())
    dynasty = Dynasty.query.get_or_404(uid)
    authors = dynasty.authors.order_by(db.func.random()).limit(5)
    return render_template('dynasty/dynasty/dynasty.html', dynasty=dynasty, authors=authors,
                           dynasties=dynasties)


@bp.route('/dynasty/add', methods=['GET', 'POST'])
@AdminPermission()
def add():
    """添加朝代"""
    form = DynastyForm()
    if form.validate_on_submit():
        dynasty = Dynasty(**form.data)
        db.session.add(dynasty)
        db.session.commit()
        return redirect(url_for('.view', uid=dynasty.id))
    return render_template('dynasty/add/add.html', form=form)


@bp.route('/dynasty/<int:dynasty_id>/edit', methods=['GET', 'POST'])
@AdminPermission()
def edit(dynasty_id):
    """编辑朝代"""
    dynasty = Dynasty.query.get_or_404(dynasty_id)
    form = DynastyForm(obj=dynasty)
    if form.validate_on_submit():
        form.populate_obj(dynasty)
        db.session.add(dynasty)
        db.session.commit()
        return redirect(url_for('.view', uid=dynasty.id))
    return render_template('dynasty/edit/edit.html', dynasty=dynasty, form=form)
