# coding: utf-8
from flask import g, redirect, url_for, abort, flash
from permission import Rule
from application.models import Topic, WorkImage, WorkReview


class VisitorRule(Rule):
    def check(self):
        return not g.user

    def deny(self):
        return redirect(url_for('site.index'))


class UserRule(Rule):
    def check(self):
        return g.user

    def deny(self):
        abort(403)


class AdminRule(Rule):
    def base(self):
        return UserRule()

    def check(self):
        return g.user.is_admin

    def deny(self):
        abort(403)


class SuperAdminRule(Rule):
    def base(self):
        return UserRule()

    def check(self):
        return g.user.is_super_admin

    def deny(self):
        abort(403)


class TopicOwnerRule(Rule):
    def __init__(self, topic_id):
        self.topic_id = topic_id
        super(TopicOwnerRule, self).__init__()

    def base(self):
        return UserRule()

    def check(self):
        topic = Topic.query.get_or_404(self.topic_id)
        return topic.user_id == g.user.id

    def deny(self):
        abort(403)


class WorkReviewOwnerRule(Rule):
    def __init__(self, work_review_id):
        self.work_review_id = work_review_id
        super(WorkReviewOwnerRule, self).__init__()

    def base(self):
        return UserRule()

    def check(self):
        work_review = WorkReview.query.get_or_404(self.work_review_id)
        return work_review.user_id == g.user.id

    def deny(self):
        abort(403)


class WorkImageOwnerRule(Rule):
    def __init__(self, work_image_id):
        self.work_image_id = work_image_id
        super(WorkImageOwnerRule, self).__init__()

    def base(self):
        return UserRule()

    def check(self):
        work_image = WorkImage.query.get_or_404(self.work_image_id)
        return work_image.user_id == g.user.id

    def deny(self):
        abort(403)