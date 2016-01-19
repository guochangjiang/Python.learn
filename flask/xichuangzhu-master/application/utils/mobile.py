# coding: utf-8
import os
import re
from werkzeug.security import gen_salt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..models import db, Work, Author, Dynasty, Quote, Collection, CollectionKind, CollectionWork


def generate_main_db():
    """生成SQLite3数据库文件"""
    from .mobile_models import _Author, _Collection, _CollectionKind, _CollectionWork, _Dynasty, _Quote, _Version, \
        _Work, Base

    db_file_path = "/tmp/xcz.db"
    if os.path.isfile(db_file_path):
        os.remove(db_file_path)

    engine = create_engine('sqlite:///%s' % db_file_path)
    Session = sessionmaker(bind=engine)
    session = Session()
    # 如果没有这一行，会报：
    # AttributeError: 'Session' object has no attribute '_model_changes'
    # 具体见：
    # http://stackoverflow.com/questions/20201809/sqlalchemy-flask-attributeerror-session-object
    # -has-no-attribute-model-chan
    session._model_changes = {}
    Base.metadata.create_all(engine)

    # 设置version
    version = _Version(version=gen_salt(20))
    session.add(version)

    # 转存作品
    works = Work.query.filter(Work.highlight).order_by(db.func.random())
    for index, work in enumerate(works):
        _work = _Work()

        _work.id = work.id
        _work.show_order = index
        _work.baidu_wiki = work.baidu_wiki
        _work.author_id = work.author_id
        _work.author = work.author.name
        _work.author_tr = work.author.name_tr
        _work.dynasty = work.author.dynasty.name
        _work.dynasty_tr = work.author.dynasty.name_tr
        _work.kind = work.type.en
        _work.kind_cn = work.type.cn
        _work.kind_cn_tr = work.type.cn_tr
        _work.foreword = work.foreword
        _work.foreword_tr = work.foreword_tr
        _work.title = work.mobile_title or work.title
        _work.title_tr = work.mobile_title_tr or work.title_tr
        _work.full_title = _get_work_full_title(work)
        _work.full_title_tr = _get_work_full_title(work, tr=True)
        _work.content = _get_work_content(work)
        _work.content_tr = _get_work_content(work, tr=True)
        _work.intro = work.intro.replace('\r\n\r\n', '\n')
        _work.intro_tr = work.intro_tr.replace('\r\n\r\n', '\n')
        _work.layout = work.layout
        _work.updated_at = work.updated_at.strftime('%Y-%m-%d %H:%M:%S')

        session.add(_work)

    # 转存文学家
    for author in Author.query.filter(Author.works.any(Work.highlight)).order_by(
            Author.birth_year.asc()):
        # 处理birth_year
        birth_year = author.birth_year
        if birth_year and '?' not in birth_year:
            birth_year += "年"
        if '-' in birth_year:
            birth_year = birth_year.replace('-', '前')

        # 处理death_year
        death_year = author.death_year
        if death_year and '?' not in death_year:
            death_year += "年"
        if '-' in death_year:
            death_year = death_year.replace('-', '前')

        _author = _Author()
        _author.id = author.id
        _author.name = author.name
        _author.name_tr = author.name_tr
        _author.intro = author.intro
        _author.intro_tr = author.intro_tr
        _author.dynasty = author.dynasty.name
        _author.dynasty_tr = author.dynasty.name_tr
        _author.birth_year = birth_year
        _author.death_year = death_year
        _author.baidu_wiki = author.baidu_wiki
        _author.updated_at = author.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        _author.works_count = author.works.filter(Work.highlight).count()
        _author.first_char = _get_first_char(author.name)

        session.add(_author)

    # 转存朝代
    for dynasty in Dynasty.query.filter(Dynasty.authors.any(Author.works.any(Work.highlight))):
        _dynasty = _Dynasty()

        _dynasty.id = dynasty.id
        _dynasty.name = dynasty.name
        _dynasty.name_tr = dynasty.name_tr
        _dynasty.intro = dynasty.intro
        _dynasty.intro_tr = dynasty.intro_tr
        _dynasty.start_year = dynasty.start_year
        _dynasty.end_year = dynasty.end_year

        session.add(_dynasty)

    # 转存摘录
    for quote in Quote.query.filter(Quote.work.has(Work.highlight)):
        _quote = _Quote()

        _quote.id = quote.id
        _quote.quote = quote.quote
        _quote.quote_tr = quote.quote_tr
        _quote.author_id = quote.work.author_id
        _quote.author = quote.work.author.name
        _quote.author_tr = quote.work.author.name_tr
        _quote.work_id = quote.work_id
        _quote.work = quote.work.title
        _quote.work_tr = quote.work.title_tr
        _quote.updated_at = quote.updated_at.strftime('%Y-%m-%d %H:%M:%S')

        session.add(_quote)

    # 转存集合类型
    for collection_kind in CollectionKind.query:
        _collection_kind = _CollectionKind()

        _collection_kind.id = collection_kind.id
        _collection_kind.show_order = collection_kind.order
        _collection_kind.name = collection_kind.name
        _collection_kind.name_tr = collection_kind.name_tr

        session.add(_collection_kind)

    # 转存集合
    for collection in Collection.query:
        _collection = _Collection()

        _collection.id = collection.id
        _collection.show_order = collection.order
        _collection.name = collection.name
        _collection.name_tr = collection.name_tr
        _collection.full_name = collection.full_name
        _collection.full_name_tr = collection.full_name_tr
        _collection.desc = collection.desc
        _collection.desc_tr = collection.desc_tr
        _collection.cover = collection.cover
        _collection.link = collection.link
        _collection.kind = collection.kind.name
        _collection.kind_tr = collection.kind.name_tr
        _collection.kind_id = collection.kind_id

        session.add(_collection)

    # 转存集合作品
    for collection_work in CollectionWork.query:
        _collection_work = _CollectionWork()

        _collection_work.id = collection_work.id
        _collection_work.show_order = collection_work.order
        _collection_work.work_id = collection_work.work_id
        _collection_work.work_title = collection_work.work.title
        _collection_work.work_title_tr = collection_work.work.title_tr
        _collection_work.work_full_title = _get_work_full_title(collection_work.work)
        _collection_work.work_full_title_tr = _get_work_full_title(collection_work.work, tr=True)
        _collection_work.work_author = collection_work.work.author.name
        _collection_work.work_author_tr = collection_work.work.author.name_tr
        _collection_work.work_dynasty = collection_work.work.author.dynasty.name
        _collection_work.work_dynasty_tr = collection_work.work.author.dynasty.name_tr
        _collection_work.work_content = _get_work_content(collection_work.work)
        _collection_work.work_content_tr = _get_work_content(collection_work.work, tr=True)
        _collection_work.collection_id = collection_work.collection_id
        _collection_work.collection = collection_work.collection.name
        _collection_work.collection_tr = collection_work.collection.name_tr

        session.add(_collection_work)

    session.commit()

    return db_file_path


def generate_user_db():
    """生成xcz_user.db"""
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy import Column, Integer, String

    db_file_path = "/tmp/xcz_user.db"

    if os.path.isfile(db_file_path):
        os.remove(db_file_path)

    engine = create_engine('sqlite:///%s' % db_file_path)
    Base = declarative_base()
    Session = sessionmaker(bind=engine)
    session = Session()
    session._model_changes = {}

    class _Like(Base):
        __tablename__ = 'likes'

        id = Column(Integer, primary_key=True)
        work_id = Column(Integer)
        show_order = Column(Integer, default=0)
        created_at = Column(String(30))

        def __repr__(self):
            return '<Like %s>' % self.work_id

    Base.metadata.create_all(engine)

    return db_file_path


def _get_work_content(work, tr=False):
    if tr:
        work_content = work.mobile_content_tr or work.content_tr
    else:
        work_content = work.mobile_content or work.content
    work_content = re.sub(r'<([^<]+)>', '', work_content)
    work_content = work_content.replace('%', "    ")
    work_content = work_content.replace('\r\n\r\n', '\n')
    return work_content


def _get_work_full_title(work, tr=False):
    if tr:
        work_title = work.mobile_title_tr or work.title_tr
        work_title_suffix = work.title_suffix_tr
    else:
        work_title = work.mobile_title or work.title
        work_title_suffix = work.title_suffix

    if work_title_suffix and '·' not in work_title:
        work_full_title = "%s · %s" % (work_title, work_title_suffix)
    else:
        work_full_title = work_title

    return work_full_title


def _get_first_char(text):
    from pypinyin import lazy_pinyin

    return lazy_pinyin(text)[0][0].upper()
