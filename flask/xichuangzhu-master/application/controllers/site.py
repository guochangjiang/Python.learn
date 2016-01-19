# coding: utf-8
from flask import render_template, Blueprint, request, get_template_attribute
from application import csrf
from ..models import db, Work, WorkImage, WorkReview, Author, Dynasty

bp = Blueprint('site', __name__)


@bp.route('/')
def index():
    """首页"""
    works = Work.query.order_by(db.func.random()).limit(4)
    work_images = WorkImage.query.order_by(WorkImage.create_time.desc()).limit(18)
    work_reviews = WorkReview.query.filter(WorkReview.is_publish).order_by(
        WorkReview.create_time.desc()).limit(4)
    authors = Author.query.order_by(db.func.random()).limit(5)
    dynasties = Dynasty.query.order_by(Dynasty.start_year.asc())
    return render_template('site/index/index.html', works=works, work_images=work_images,
                           work_reviews=work_reviews, authors=authors, dynasties=dynasties)


@csrf.exempt
@bp.route('/works', methods=['POST'])
def works():
    """生成首页需要的作品json数据"""
    works = Work.query.order_by(db.func.random()).limit(4)
    render_works = get_template_attribute('work/works/_works.html', 'render_works')
    return render_works(works, True)


@bp.route('/search')
def search():
    keyword = request.args.get('q')
    page = request.args.get('page', 1, int)
    if not keyword:
        authors = None
        works = None
    else:
        authors = Author.query.filter(Author.name.like('%%%s%%' % keyword)).limit(8)
        works = Work.query.filter(Work.title.like('%%%s%%' % keyword)).paginate(page, 15)
    return render_template('site/search/search.html', keyword=keyword, authors=authors, works=works)


@bp.route('/about')
def about():
    """关于页"""
    return render_template('site/about/about.html')


@bp.route('/disclaimer')
def disclaimer():
    """免责声明"""
    return render_template('site/disclaimer/disclaimer.html')


@bp.route('/update')
def update():
    """Just for benchmark vs Node.js"""
    import json
    from ..models import Work

    result = []
    for work in Work.query.filter(Work.highlight):
        result.append({
            'id': work.id,
            'update_at': work.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return json.dumps(result)
