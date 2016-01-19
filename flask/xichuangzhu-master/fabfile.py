# coding: utf-8
from fabric.api import run, env, cd, prefix, shell_env
from config import load_config

config = load_config()


def deploy():
    """部署"""
    env.host_string = config.HOST_STRING
    with cd('/var/www/xichuangzhu'):
        with shell_env(MODE='PRODUCTION'):
            run('git reset --hard HEAD')
            run('git pull')
            run('npm install')
            with prefix('source venv/bin/activate'):
                run('pip install -r requirements.txt')
                run('python manage.py db upgrade')
                run('python manage.py build')
            run('sudo supervisorctl restart xcz')


def pull():
    """仅更新代码"""
    env.host_string = config.HOST_STRING
    with cd('/var/www/xichuangzhu'):
        run('git pull')


def restart():
    """重启服务器"""
    env.host_string = config.HOST_STRING
    run('sudo supervisorctl restart xcz')


def convert_title():
    """转换标题"""
    env.host_string = config.HOST_STRING
    with cd('/var/www/xichuangzhu'):
        with shell_env(MODE='PRODUCTION'):
            with prefix('source venv/bin/activate'):
                run('python manage.py convert_title')


def find_works_wiki():
    """寻找作品wiki url"""
    env.host_string = config.HOST_STRING
    with cd('/var/www/xichuangzhu'):
        with shell_env(MODE='PRODUCTION'):
            with prefix('source venv/bin/activate'):
                run('python manage.py find_works_wiki')


def find_authors_wiki():
    """寻找作者wiki url"""
    env.host_string = config.HOST_STRING
    with cd('/var/www/xichuangzhu'):
        with shell_env(MODE='PRODUCTION'):
            with prefix('source venv/bin/activate'):
                run('python manage.py find_authors_wiki')
