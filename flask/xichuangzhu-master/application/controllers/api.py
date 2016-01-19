# coding: utf-8
from flask import Blueprint
from jinja2 import Markup
from ..models import db, Quote, Work, Author
from application.utils.helpers import jsonify, absolute_url_for
from application.utils.filters import markdown_work, markdown

bp = Blueprint('api', __name__)


@bp.route('/api/get_random_quote')
@jsonify
def get_random_quote():
    quote = Quote.query.order_by(db.func.random()).first()
    return {
        'quote': quote.quote,
        'author': quote.author.name,
        'work': quote.work.title,
        'url': absolute_url_for('work.view', work_id=quote.work_id)
    }


@bp.route('/api/get_random_work')
@jsonify
def get_random_work():
    work = Work.query.order_by(db.func.random()).first()
    content = work.content if not work.mobile_content else work.mobile_content
    return {
        'id': work.id,
        'title': work.title,
        'content': Markup(markdown_work(content)),
        'intro': Markup(markdown(work.intro)) if work.intro else "",
        'author': work.author.name,
        'author_id': work.author_id,
        'dynasty': work.author.dynasty.name,
        'dynasty_id': work.author.dynasty_id
    }


@bp.route('/api/get_author/<int:uid>')
@jsonify
def get_author(uid):
    author = Author.query.get_or_404(uid)
    return {
        'id': uid,
        'name': author.name,
        'dynasty': author.dynasty.name,
        'dynasty_id': author.dynasty_id,
        'intro': author.intro,
        'works': [{'id': work.id, 'title': work.title} for work in author.works]
    }
