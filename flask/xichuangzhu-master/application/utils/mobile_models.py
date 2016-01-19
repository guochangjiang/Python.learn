# coding: utf-8
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum, Text

Base = declarative_base()


class _Version(Base):
    __tablename__ = 'version'

    version = Column(String(20), primary_key=True)


class _Work(Base):
    __tablename__ = 'works'

    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    full_title = Column(String(50))
    show_order = Column(Integer)
    author = Column(String(50))
    author_id = Column(Integer)
    dynasty = Column(String(10))
    kind = Column(Enum('shi', 'ci', 'qu', 'fu', 'wen'))
    kind_cn = Column(String(20))
    baidu_wiki = Column(String(200))
    foreword = Column(Text)
    content = Column(Text)
    intro = Column(Text)
    layout = Column(String(10))
    updated_at = Column(String(30))

    # 繁体
    title_tr = Column(String(50))
    full_title_tr = Column(String(50))
    author_tr = Column(String(50))
    dynasty_tr = Column(String(10))
    kind_cn_tr = Column(String(20))
    foreword_tr = Column(Text)
    content_tr = Column(Text)
    intro_tr = Column(Text)

    def __repr__(self):
        return '<Work %s>' % self.title


class _Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    first_char = Column(String(10))
    intro = Column(Text)
    works_count = Column(Integer)
    dynasty = Column(String(10))
    birth_year = Column(String(20))
    death_year = Column(String(20))
    updated_at = Column(String(30))
    baidu_wiki = Column(String(200))

    # 繁体
    name_tr = Column(String(50))
    intro_tr = Column(Text)
    dynasty_tr = Column(String(10))


class _Dynasty(Base):
    __tablename__ = 'dynasties'

    id = Column(Integer, primary_key=True)
    name = Column(String(10))
    intro = Column(Text)
    start_year = Column(Integer)
    end_year = Column(Integer)

    # 繁体
    name_tr = Column(String(10))
    intro_tr = Column(Text)


class _Quote(Base):
    __tablename__ = 'quotes'

    id = Column(Integer, primary_key=True)
    quote = Column(Text)
    author_id = Column(Integer)
    author = Column(String(10))
    work_id = Column(Integer)
    work = Column(String(50))
    updated_at = Column(String(30))

    # 繁体
    quote_tr = Column(Text)
    author_tr = Column(String(10))
    work_tr = Column(String(50))


class _Collection(Base):
    __tablename__ = 'collections'

    id = Column(Integer, primary_key=True)
    show_order = Column(Integer)
    name = Column(String(200))
    full_name = Column(String(200))
    abbr = Column(String(50))
    desc = Column(Text())
    cover = Column(String(200))
    link = Column(String(300))
    kind_id = Column(Integer)
    kind = Column(String(100))

    name_tr = Column(String(200))
    full_name_tr = Column(String(200))
    abbr_tr = Column(String(50))
    desc_tr = Column(Text())
    kind_tr = Column(String(100))


class _CollectionKind(Base):
    __tablename__ = 'collection_kinds'

    id = Column(Integer, primary_key=True)
    show_order = Column(Integer)
    name = Column(String(100))

    # 繁体
    name_tr = Column(String(100))


class _CollectionWork(Base):
    __tablename__ = 'collection_works'

    id = Column(Integer, primary_key=True)
    show_order = Column(Integer)

    work_id = Column(Integer)
    work_title = Column(String(100))
    work_full_title = Column(String(50))
    work_author = Column(String(50))
    work_dynasty = Column(String(10))
    work_content = Column(Text)
    collection_id = Column(Integer)
    collection = Column(String(100))

    # 繁体
    work_title_tr = Column(String(100))
    work_full_title_tr = Column(String(50))
    work_author_tr = Column(String(50))
    work_dynasty_tr = Column(String(10))
    work_content_tr = Column(Text)
    collection_tr = Column(String(100))
