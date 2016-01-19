# coding: utf-8
import os
import glob2
import requests
from lxml import html
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from fabric.api import run as fabrun, env
from application import create_app
from application.models import db, Work, Author, Dynasty, Quote, Collection, CollectionKind

# Used by app debug & livereload
PORT = 5000

app = create_app()
manager = Manager(app)

# 添加migrate命令
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def run():
    """启动app"""
    app.run(debug=True, port=PORT)


@manager.command
def build():
    """Use FIS to compile assets."""
    os.system('gulp')
    os.chdir('application')
    os.system('fis release -d ../output -opmD')


@manager.command
def live():
    """Run livereload server"""
    from livereload import Server

    server = Server(app)

    map(server.watch, glob2.glob("application/pages/**/*.*"))  # pages
    map(server.watch, glob2.glob("application/macros/**/*.html"))  # macros
    map(server.watch, glob2.glob("application/static/**/*.*"))  # public assets

    server.serve(port=PORT)


@manager.command
def syncdb():
    """根据model创建数据库tables"""
    db.create_all()


@manager.command
def backdb():
    """将数据库中的表结构和数据提取为sql文件"""
    env.host_string = "localhost"
    fabrun("mysqldump -uroot -p xcz > /var/www/xichuangzhu/xcz.sql")


@manager.command
@manager.command
@manager.command
def convert_tr():
    with app.app_context():
        for work in Work.query:
            print("work - %d" % work.id)
            work.populate_tr_fields()
            db.session.add(work)
            db.session.commit()
        for quote in Quote.query:
            print("quote - %d" % quote.id)
            quote.populate_tr_fields()
            db.session.add(quote)
            db.session.commit()
        for author in Author.query:
            print("author - %d" % author.id)
            author.populate_tr_fields()
            db.session.add(author)
            db.session.commit()
        for dynasty in Dynasty.query:
            print("dynasty - %d" % dynasty.id)
            dynasty.populate_tr_fields()
            db.session.add(dynasty)
            db.session.commit()
        for collection in Collection.query:
            print("collection - %d" % collection.id)
            collection.populate_tr_fields()
            db.session.add(collection)
            db.session.commit()
        for collection_kind in CollectionKind.query:
            print("collection kind - %d" % collection_kind.id)
            collection_kind.populate_tr_fields()
            db.session.add(collection_kind)
            db.session.commit()


@manager.command
def detect_whitespace():
    with app.app_context():
        for work in Work.query:
            if ' ' in work.content:
                index = work.content.index(' ')
                print("work %d - %d" % (work.id, index))
        for quote in Quote.query:
            if ' ' in quote.quote:
                index = quote.quote.index(' ')
                print("quote %d - %d" % (quote.id, index))


@manager.command
def detect_illegal_punctuation():
    with app.app_context():
        for work in Work.query:
            for letter in ',()?-:':
                if letter in work.content:
                    print("work %d %s" % (work.id, letter))
        for quote in Quote.query:
            for letter in ',()?-:':
                if letter in quote.quote:
                    print("work %d %s" % (quote.id, letter))


@manager.command
def uniform_content():
    with app.app_context():
        for work in Work.query:
            print("work %d", work.id)
            work.content = _uniform_content(work.content)
            work.mobile_content = _uniform_content(work.mobile_content)
            work.foreword = _uniform_content(work.foreword)
            work.intro = _uniform_content(work.intro)
            db.session.add(work)
            db.session.commit()

        for quote in Quote.query:
            print("quote %d", quote.id)
            quote.quote = _uniform_content(quote.quote)
            db.session.add(quote)
            db.session.commit()

        for author in Author.query:
            print("author %d", author.id)
            author.intro = _uniform_content(author.intro)
            db.session.add(author)
            db.session.commit()


@manager.command
def find_works_wiki():
    with app.app_context():
        for work in Work.query:
            if work.baidu_wiki:
                continue

            title = work.title
            if work.title_suffix:
                title += '' + work.title_suffix
            print(title)

            r = requests.get('http://baike.baidu.com/search?word=%s&pn=0&rn=0&enc=utf8' % title)
            tree = html.fromstring(r.text)
            results = tree.cssselect('.search-list dd a')
            if len(results) > 0:
                work.baidu_wiki = results[0].get('href')
                print(work.baidu_wiki)
                db.session.add(work)
                db.session.commit()


@manager.command
def find_authors_wiki():
    with app.app_context():
        for author in Author.query:
            if author.baidu_wiki:
                continue
            print(author.name)

            r = requests.get('http://baike.baidu.com/search?word=%s&pn=0&rn=0&enc=utf8' % author.name)
            tree = html.fromstring(r.text)
            results = tree.cssselect('.search-list dd a')
            if len(results) > 0:
                author.baidu_wiki = results[0].get('href')
                print(author.baidu_wiki)
                db.session.add(author)
                db.session.commit()


def _uniform_content(content):
    if not content:
        return ""
    return content \
        .replace(' ', '') \
        .replace(',', '，') \
        .replace('(', '（') \
        .replace(')', '）') \
        .replace('?', '？') \
        .replace('-', '·') \
        .replace(':', '：')


if __name__ == "__main__":
    manager.run()
