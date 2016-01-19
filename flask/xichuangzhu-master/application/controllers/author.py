# coding: utf-8
import datetime

from flask import render_template, request, redirect, url_for, Blueprint
from ..models import db, Author, Quote, Work, WorkType, CollectWork, Dynasty
from application.utils.permissions import AdminPermission
from ..forms import AuthorForm

bp = Blueprint('author', __name__)


@bp.route('/author/<author_id>')
def view(author_id):
    """文学家主页"""
    author = Author.query.get_or_404(author_id)
    # 获取1条摘录
    quote_id = request.args.get('q')
    quote = Quote.query.get(quote_id) if quote_id else None
    if not quote:
        quote = author.random_quote
    # 随机获取10条以下的摘录
    if AdminPermission().check():
        quotes = author.quotes
    else:
        quotes = author.quotes.order_by(db.func.random()).limit(10)
    stmt = db.session.query(Work.type_id, db.func.count(Work.type_id).label('type_num')).filter(
        Work.author_id == author.id).group_by(Work.type_id).subquery()
    work_types = db.session.query(WorkType, stmt.c.type_num) \
        .join(stmt, WorkType.id == stmt.c.type_id)
    return render_template('author/author/author.html', author=author, quote=quote, work_types=work_types,
                           quotes=quotes)


@bp.route('/authors')
def authors():
    """全部文学家"""
    # 仅获取包含至少1个文学家的朝代
    dynasties = Dynasty.query.filter(Dynasty.authors.any()).order_by(Dynasty.start_year.asc())
    # get the authors who's works are latest collected by user
    stmt = db.session.query(Author.id, CollectWork.create_time).join(Work).join(
        CollectWork).group_by(Author.id).having(
        db.func.max(CollectWork.create_time)).subquery()
    hot_authors = Author.query.join(stmt, Author.id == stmt.c.id).order_by(
        stmt.c.create_time.desc()).limit(8)
    return render_template('author/authors/authors.html', dynasties=dynasties, hot_authors=hot_authors)


@bp.route('/author/add', methods=['GET', 'POST'])
@AdminPermission()
def add():
    """添加文学家"""
    form = AuthorForm()
    form.dynasty_id.choices = [(d.id, d.name) for d in Dynasty.query.order_by(Dynasty.start_year)]
    if form.validate_on_submit():
        author = Author(**form.data)
        author.populate_tr_fields()
        db.session.add(author)
        db.session.commit()
        return redirect(url_for('.view', author_id=author.id))
    return render_template('author/add/add.html', form=form)


@bp.route('/author/<int:author_id>/edit', methods=['GET', 'POST'])
@AdminPermission()
def edit(author_id):
    """编辑文学家"""
    author = Author.query.get_or_404(author_id)
    form = AuthorForm(obj=author)
    form.dynasty_id.choices = [(d.id, d.name) for d in Dynasty.query.order_by(Dynasty.start_year)]
    if form.validate_on_submit():
        form.populate_obj(author)
        author.updated_at = datetime.datetime.now()
        author.populate_tr_fields()
        db.session.add(author)
        db.session.commit()
        return redirect(url_for('.view', author_id=author.id))
    return render_template('author/edit/edit.html', author=author, form=form)


@bp.route('/author/quote/<int:quote_id>/delete')
@AdminPermission()
def delete_quote(quote_id):
    """删除摘录"""
    quote = Quote.query.get_or_404(quote_id)
    db.session.delete(quote)
    db.session.commit()
    return redirect(url_for('.view', author_id=quote.author.id))
