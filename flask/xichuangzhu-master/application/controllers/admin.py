# coding: utf-8
from flask import render_template, Blueprint, request, send_file
from ..models import Work, Author, Dynasty, WorkType, Quote, CollectionKind, Collection, CollectionWork
from application.utils.permissions import AdminPermission
from application.utils.mobile import generate_main_db as _generate_main_db, generate_user_db as _generate_user_db

bp = Blueprint('admin', __name__)


@bp.route('/admin/authors', defaults={'page': 1})
@bp.route('/admin/authors/<int:page>', methods=['GET', 'POST'])
@AdminPermission()
def authors(page):
    """管理文学家"""
    paginator = Author.query.paginate(page, 30)
    return render_template('admin/authors/authors.html', paginator=paginator)


@bp.route('/admin/works', defaults={'page': 1})
@bp.route('/admin/works/page/<int:page>', methods=['GET', 'POST'])
@AdminPermission()
def works(page):
    """管理作品"""
    paginator = Work.query.paginate(page, 15)
    return render_template('admin/works/works.html', paginator=paginator)


@bp.route('/admin/highlight_works', defaults={'page': 1})
@bp.route('/admin/highlight_works/page/<int:page>', methods=['GET', 'POST'])
@AdminPermission()
def highlight_works(page):
    """全部加精作品"""
    # 查询条件
    work_type = request.args.get('type')
    dynasty_id = request.args.get('dynasty_id', type=int)

    # 符合条件的作品
    works = Work.query.filter(Work.highlight)
    if work_type:
        works = works.filter(Work.type.has(WorkType.en == work_type))
    if dynasty_id:
        works = works.filter(Work.author.has(Author.dynasty.has(Dynasty.id == dynasty_id)))
    works = works.order_by(Work.highlight_at.desc())
    paginator = works.paginate(page, 15)

    work_types = WorkType.query
    dynasties = Dynasty.query.order_by(Dynasty.start_year.asc())

    authors_count = Author.query.filter(Author.works.any(Work.highlight)).count()
    works_count = Work.query.filter(Work.highlight).count()
    quotes_count = Quote.query.filter(Quote.work.has(Work.highlight)).count()
    return render_template('admin/highlight_works/highlight_works.html', paginator=paginator, work_type=work_type,
                           dynasty_id=dynasty_id, work_types=work_types, dynasties=dynasties,
                           authors_count=authors_count, works_count=works_count,
                           quotes_count=quotes_count)


@bp.route('/admin/unhighlight_works', defaults={'page': 1})
@bp.route('/admin/unhighlight_works/page/<int:page>', methods=['GET', 'POST'])
@AdminPermission()
def unhighlight_works(page):
    """全部未加精作品"""
    works = Work.query.filter(~Work.highlight).paginate(page, 15)
    return render_template('admin/unhighlight_works/unhighlight_works.html', works=works)


@bp.route('/admin/quotes', defaults={'page': 1})
@bp.route('/admin/quotes/page/<int:page>', methods=['GET', 'POST'])
@AdminPermission()
def quotes(page):
    """管理摘录"""
    paginator = Quote.query.order_by(Quote.created_at.desc()).paginate(page, 20)
    return render_template('admin/quotes/quotes.html', paginator=paginator)


@bp.route('/admin/collections')
@AdminPermission()
def collections():
    """管理选集"""
    collection_kinds = CollectionKind.query.order_by(CollectionKind.order.asc())
    return render_template('admin/collections/collections.html', collection_kinds=collection_kinds)


@bp.route('/admin/collection/<int:uid>/works')
@AdminPermission()
def collection_works(uid):
    """管理选集作品"""
    collection = Collection.query.get_or_404(uid)
    return render_template('admin/collection_works/collection_works.html', collection=collection)


@bp.route('/admin/generate_main_db')
@AdminPermission()
def generate_main_db():
    db_path = _generate_main_db()
    return send_file(db_path, as_attachment=True)


@bp.route('/admin/generate_user_dbs')
@AdminPermission()
def generate_user_db():
    db_path = _generate_user_db()
    return send_file(db_path, as_attachment=True)
