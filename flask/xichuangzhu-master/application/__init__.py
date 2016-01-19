# coding: utf-8
import sys

import os


# 将project目录加入sys.path
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_path not in sys.path:
    sys.path.insert(0, project_path)

import logging
import jinja2
from flask import Flask, request, url_for, g, render_template, flash
from werkzeug.wsgi import SharedDataMiddleware
from datetime import time
from flask_wtf.csrf import CsrfProtect
from flask.ext.uploads import configure_uploads
from flask_debugtoolbar import DebugToolbarExtension
from six import iteritems
from application.utils.helpers import get_current_user, signout_user
from config import load_config
from imp import reload
# convert python's encoding to utf8
#reload(sys)
#sys.setdefaultencoding('utf-8')

csrf = CsrfProtect()


def create_app():
    app = Flask(__name__)
    config = load_config()
    app.config.from_object(config)

    # CSRF protect
    csrf.init_app(app)

    if app.debug or app.testing:
        DebugToolbarExtension(app)

        # Serve static files
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/pages': os.path.join(app.config.get('PROJECT_PATH'), 'application/pages')
        })
    else:
        # Log errors to stderr in production mode
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.ERROR)

        if app.config.get('SENTRY_DSN'):
            from application.utils.sentry import sentry

            sentry.init_app(app, dsn=app.config.get('SENTRY_DSN'))

        # Serve static files
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/static': os.path.join(app.config.get('PROJECT_PATH'), 'output/static'),
            '/pkg': os.path.join(app.config.get('PROJECT_PATH'), 'output/pkg'),
            '/pages': os.path.join(app.config.get('PROJECT_PATH'), 'output/pages')
        })

    from application.utils.mails import mail

    mail.init_app(app)

    register_db(app)
    register_routes(app)
    register_jinja(app)
    register_error_handle(app)
    register_logger(app)
    register_uploadsets(app)
    register_hooks(app)

    return app


def register_jinja(app):
    from application.utils import permissions
    from application.utils import filters

    if app.debug or app.testing:
        my_loader = jinja2.ChoiceLoader([
            app.jinja_loader,
            jinja2.FileSystemLoader([
                os.path.join(app.config.get('PROJECT_PATH'), 'application/macros'),
                os.path.join(app.config.get('PROJECT_PATH'), 'application/pages')
            ])
        ])
    else:
        my_loader = jinja2.ChoiceLoader([
            app.jinja_loader,
            jinja2.FileSystemLoader([
                os.path.join(app.config.get('PROJECT_PATH'), 'output/macros'),
                os.path.join(app.config.get('PROJECT_PATH'), 'output/pages')
            ])
        ])
    app.jinja_loader = my_loader

    # Filters
    app.jinja_env.filters.update({
        'clean_work': filters.clean_work,
        'timesince': filters.timesince,
        'markdown_work': filters.markdown_work,
        'markdown': filters.markdown,
        'format_year': filters.format_year,
        'format_text': filters.format_text,
        'is_work_collected': filters.is_work_collected,
        'is_work_image_collected': filters.is_work_image_collected
    })

    # Url generator for pagination
    def url_for_other_page(page):
        view_args = request.view_args.copy()
        args = request.args.copy().to_dict()
        args['page'] = page
        view_args.update(args)
        return url_for(request.endpoint, **view_args)

    def set_url_param(**params):
        """Set param in url"""
        view_args = request.view_args.copy()
        args = request.args.copy().to_dict()
        combined_args = dict(view_args.items() + args.items())
        if params:
            combined_args.update(params)
        return url_for(request.endpoint, **combined_args)

    rules = {}
    for endpoint, _rules in iteritems(app.url_map._rules_by_endpoint):
        if any(item in endpoint for item in ['_debug_toolbar', 'debugtoolbar', 'static']):
            continue
        rules[endpoint] = [{'rule': rule.rule} for rule in _rules]

    app.jinja_env.globals.update({
        'url_for_other_page': url_for_other_page,
        'set_url_param': set_url_param,
        'rules': rules,
        'permissions': permissions
    })


def register_logger(app):
    """Send error log to admin by smtp"""
    pass


def register_db(app):
    from .models import db

    db.init_app(app)


def register_routes(app):
    """Register routes."""
    from . import controllers
    from flask.blueprints import Blueprint

    for module in _import_submodules_from_package(controllers):
        bp = getattr(module, 'bp')
        if bp and isinstance(bp, Blueprint):
            app.register_blueprint(bp)


def register_error_handle(app):
    @app.errorhandler(403)
    def page_403(error):
        return render_template('site/403/403.html'), 403

    @app.errorhandler(404)
    def page_404(error):
        return render_template('site/404/404.html'), 404

    @app.errorhandler(500)
    def page_500(error):
        return render_template('site/500/500.html'), 500


def register_hooks(app):
    """Register hooks."""

    @app.before_request
    def before_request():
        g.user = get_current_user()
        if g.user:
            if g.user.is_new:
                flash('请登录邮箱激活账户。')
                signout_user()
            if g.user.is_banned:
                flash('账户已被禁用，请联系管理员。')
                signout_user()

        if g.user and g.user.is_admin:
            g._before_request_time = time.time()

    @app.after_request
    def after_request(response):
        if hasattr(g, '_before_request_time'):
            delta = time.time() - g._before_request_time
            response.headers['X-Render-Time'] = delta * 1000
        return response


def register_uploadsets(app):
    from application.utils.uploadsets import workimages

    configure_uploads(app, (workimages))


def _get_template_name(template_reference):
    """Get current template name."""
    return template_reference._TemplateReference__context.name


def _import_submodules_from_package(package):
    import pkgutil

    modules = []
    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__,
                                                         prefix=package.__name__ + "."):
        modules.append(__import__(modname, fromlist="dummy"))
    return modules
