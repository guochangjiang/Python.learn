# coding: utf-8
from flask import render_template, redirect, url_for, Blueprint, g
from ..models import db, Topic, TopicComment
from ..forms import TopicForm, TopicCommentForm
from application.utils.permissions import UserPermission, TopicAdminPermission

bp = Blueprint('topic', __name__)


@bp.route('/topic/<int:topic_id>', methods=['POST', 'GET'])
def view(topic_id):
    """话题"""
    form = TopicCommentForm()
    topic = Topic.query.get_or_404(topic_id)
    topic.click_num += 1
    db.session.add(topic)
    db.session.commit()
    if form.validate_on_submit():
        permission = UserPermission()
        if not permission.check():
            return permission.deny()
        comment = TopicComment(user_id=g.user.id, topic_id=topic_id, **form.data)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('.view', topic_id=topic_id) + "#" + str(comment.id))
    return render_template('topic/topic/topic.html', topic=topic, form=form)


@bp.route('/topics', defaults={'page': 1})
@bp.route('/topics/page/<int:page>')
def topics(page):
    """全部话题"""
    paginator = Topic.query.order_by(Topic.create_time.desc()).paginate(page, 10)
    return render_template('topic/topics/topics.html', paginator=paginator)


@bp.route('/topic/add', methods=['POST', 'GET'])
@UserPermission()
def add():
    """添加话题"""
    form = TopicForm()
    if form.validate_on_submit():
        topic = Topic(user_id=g.user.id, **form.data)
        db.session.add(topic)
        db.session.commit()
        return redirect(url_for('.view', topic_id=topic.id))
    return render_template('topic/add/add.html', form=form)


@bp.route('/topic/<int:topic_id>/edit', methods=['POST', 'GET'])
def edit(topic_id):
    """编辑话题"""
    topic = Topic.query.get_or_404(topic_id)
    permission = TopicAdminPermission(topic_id)
    if not permission.check():
        return permission.deny()
    form = TopicForm(obj=topic)
    if form.validate_on_submit():
        form.populate_obj(topic)
        db.session.add(topic)
        db.session.commit()
        return redirect(url_for('.view', topic_id=topic_id))
    return render_template('topic/edit/edit.html', topic=topic, form=form)


@bp.route('/topic/<int:topic_id>/delete')
def delete(topic_id):
    """删除话题"""
    topic = Topic.query.get_or_404(topic_id)
    permission = TopicAdminPermission(topic_id)
    if not permission.check():
        return permission.deny()
    db.session.delete(topic)
    db.session.commit()
    return redirect(url_for('.topics'))
