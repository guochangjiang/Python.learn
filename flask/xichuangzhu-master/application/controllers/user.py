# coding: utf-8
from __future__ import division
from flask import render_template, Blueprint, g
from ..models import User, CollectWork, CollectWorkImage, Work, WorkImage, WorkReview
from application.utils.helpers import check_is_me
from application.utils.permissions import UserPermission

bp = Blueprint('user', __name__)


@bp.route('/people/<user_abbr>')
def view(user_abbr):
    """用户主页"""
    user = User.query.filter(User.abbr == user_abbr).first_or_404()
    query = user.work_reviews
    if not check_is_me(user.id):
        query = query.filter(WorkReview.is_publish == True)
    work_reviews = query.limit(3)
    work_reviews_num = query.count()
    topics = user.topics.limit(3)
    work_images = user.work_images.limit(16)
    return render_template('user/user/user.html', user=user, work_reviews=work_reviews,
                           work_reviews_num=work_reviews_num, topics=topics,
                           work_images=work_images)


@bp.route('/people/<user_abbr>/work_reviews', defaults={'page': 1})
@bp.route('/people/<user_abbr>/work_reviews/page/<int:page>')
def work_reviews(user_abbr, page):
    """用户的作品点评"""
    user = User.query.filter(User.abbr == user_abbr).first_or_404()
    work_reviews = user.work_reviews
    if not check_is_me(user.id):
        work_reviews = work_reviews.filter(WorkReview.is_publish == True)
    paginator = work_reviews.paginate(page, 10)
    return render_template('user/work_reviews/work_reviews.html', user=user, paginator=paginator)


@bp.route('/people/<user_abbr>/topics', defaults={'page': 1})
@bp.route('/people/<user_abbr>/topics/page/<int:page>')
def topics(user_abbr, page):
    """用户发表的话题"""
    user = User.query.filter(User.abbr == user_abbr).first_or_404()
    paginator = user.topics.paginate(page, 10)
    return render_template('user/topics/topics.html', user=user, paginator=paginator)


@bp.route('/people/<user_abbr>/work_images', defaults={'page': 1})
@bp.route('/people/<user_abbr>/work_images/page/<int:page>')
def work_images(user_abbr, page):
    """用户上传的作品图片"""
    user = User.query.filter(User.abbr == user_abbr).first_or_404()
    paginator = user.work_images.paginate(page, 16)
    return render_template('user/work_images/work_images.html', user=user, paginator=paginator)


@bp.route('/me/collects', defaults={'page': 1})
@bp.route('/me/collects/<int:page>')
@UserPermission()
def collects(page):
    """用户收藏页"""
    paginator = Work.query.join(CollectWork).filter(CollectWork.user_id == g.user.id).order_by(
        CollectWork.create_time.desc()).paginate(page, 8)
    collect_work_images = WorkImage.query.join(CollectWorkImage).filter(
        CollectWorkImage.user_id == g.user.id).order_by(
        CollectWorkImage.create_time.desc()).limit(9)
    return render_template('user/collects/collects.html', user=g.user, paginator=paginator,
                           collect_work_images=collect_work_images)


@bp.route('/me/collect_works', defaults={'page': 1})
@bp.route('/me/collect_works/page/<int:page>')
@UserPermission()
def collect_works(page):
    """用户收藏的文学作品"""
    paginator = Work.query.join(CollectWork).filter(
        CollectWork.user_id == g.user.id).order_by(
        CollectWork.create_time.desc()).paginate(page, 10)
    return render_template('user/collect_works/collect_works.html', paginator=paginator)


@bp.route('/me/collect_work_images', defaults={'page': 1})
@bp.route('/me/collect_work_images/page/<int:page>')
@UserPermission()
def collect_work_images(page):
    """用户收藏的图片"""
    paginator = WorkImage.query.join(CollectWorkImage).filter(
        CollectWorkImage.user_id == g.user.id).order_by(
        CollectWorkImage.create_time.desc()).paginate(page, 12)
    return render_template('user/collect_work_images/collect_work_images.html', paginator=paginator)
