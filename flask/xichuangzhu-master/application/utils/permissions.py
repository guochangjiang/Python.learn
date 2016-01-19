# coding: utf-8
from permission import Permission
from application.utils.rules import UserRule, AdminRule, SuperAdminRule, TopicOwnerRule, \
    WorkImageOwnerRule, WorkReviewOwnerRule, VisitorRule


class VisitorPermission(Permission):
    def rule(self):
        return VisitorRule()


class UserPermission(Permission):
    def rule(self):
        return UserRule()


class AdminPermission(Permission):
    def rule(self):
        return AdminRule() | SuperAdminRule()


class SuperAdminPermission(Permission):
    def rule(self):
        return SuperAdminRule()


class TopicAdminPermission(Permission):
    def __init__(self, topic_id):
        self.topic_id = topic_id
        super(TopicAdminPermission, self).__init__()

    def rule(self):
        return TopicOwnerRule(self.topic_id) | AdminRule() | SuperAdminRule()


class WorkReviewAdminPermission(Permission):
    def __init__(self, work_review_id):
        self.work_review_id = work_review_id
        super(WorkReviewAdminPermission, self).__init__()

    def rule(self):
        return WorkReviewOwnerRule(self.work_review_id) | AdminRule() | SuperAdminRule()


class WorkImageAdminPermission(Permission):
    def __init__(self, work_image_id):
        self.work_image_id = work_image_id
        super(WorkImageAdminPermission, self).__init__()

    def rule(self):
        return WorkImageOwnerRule(self.work_image_id)