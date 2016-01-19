# coding: utf-8
import hashlib

import requests
from flask import render_template, request, redirect, url_for, Blueprint, flash, abort, g, \
    session, current_app
from ..models import db, User
from application.utils.helpers import signin_user, signout_user
from ..forms import SignupForm, SettingsForm
from application.utils.permissions import UserPermission, VisitorPermission
from application.utils.mails import signup_mail

bp = Blueprint('account', __name__)


@bp.route('/pre_signin')
@VisitorPermission()
def pre_signin():
    """跳转豆瓣OAuth登陆之前，记录referer"""
    session['referer'] = request.referrer
    config = current_app.config
    return redirect(config.get('DOUBAN_LOGIN_URL'))


@bp.route('/signin')
@VisitorPermission()
def signin():
    """通过豆瓣OAuth登陆"""
    # get current authed user id
    code = request.args.get('code')
    if not code:
        return redirect(url_for('site.index'))
    url = "https://www.douban.com/service/auth2/token"
    config = current_app.config
    data = {
        'client_id': config.get('DOUBAN_CLIENT_ID'),
        'client_secret': config.get('DOUBAN_SECRET'),
        'redirect_uri': config.get('DOUBAN_REDIRECT_URI'),
        'grant_type': 'authorization_code',
        'code': code
    }
    headers = {
        'User-Agent': 'request'
    }
    res = requests.post(url, data=data, headers=headers).json()
    if 'douban_user_id' not in res:
        return redirect(url_for('site.index'))
    user_id = int(res['douban_user_id'])

    user = User.query.get(user_id)
    if user:
        if user.is_banned:
            flash('账户已被禁用')
            return redirect(url_for('site.index'))
        if user.is_new:
            flash('账户尚未激活，请登陆邮箱激活账户')
            return redirect(url_for('site.index'))

        flash('欢迎来到西窗烛')
        signin_user(user, True)
        redirect_url = session.get('referer') or url_for('site.index')
        session.pop('referer')
        return redirect(redirect_url)
    # 通过加密的session传递user_id数据，防止恶意注册
    session['signup_user_id'] = user_id
    return redirect(url_for('.signup'))


@bp.route('/signup', methods=['GET', 'POST'])
@VisitorPermission()
def signup():
    """发送激活邮件"""
    if not 'signup_user_id' in session:
        abort(403)

    user_id = int(session['signup_user_id'])
    user = User.query.filter(User.id == user_id).first()
    if user:
        abort(403)

    # Get user info from douban
    url = "https://api.douban.com/v2/user/%d" % user_id
    user_info = requests.get(url).json()
    form = SignupForm()
    if form.validate_on_submit():
        to_addr = form.email.data
        user = User(id=user_id, name=user_info['name'], abbr=user_info['uid'],
                    signature=user_info['signature'], email=to_addr)
        # 如果存在大图，则使用大图
        if user_info['large_avatar'] != "http://img3.douban.com/icon/user_large.jpg":
            user.avatar = user_info['large_avatar']
        else:
            user.avatar = user_info['avatar']
        db.session.add(user)
        db.session.commit()

        # send activate email
        try:
            signup_mail(user)
        except:
            flash('邮件发送失败，请稍后尝试')
        else:
            flash('激活邮件已发送到你的邮箱，请查收')

        session.pop('signup_user_id')
        return redirect(url_for('site.index'))
    return render_template('account/signup/signup.html', user_info=user_info, form=form)


@bp.route('/activate/<int:user_id>/<token>')
def activate(user_id, token):
    """激活用户"""
    user = User.query.get_or_404(user_id)
    if token == hashlib.sha1(user.name).hexdigest():
        user.is_new = False
        db.session.add(user)
        db.session.commit()
        signin_user(user, True)
        flash('账号激活成功！')
        return redirect(url_for('site.index'))
    flash('无效的激活链接')
    return redirect(url_for('site.index'))


@bp.route('/signout')
def signout():
    """登出"""
    signout_user()
    return redirect(request.referrer or url_for('site.index'))


@bp.route('/settings', methods=['GET', 'POST'])
@UserPermission()
def settings():
    """个人设置"""
    form = SettingsForm(signature=g.user.signature)
    if form.validate_on_submit():
        g.user.signature = form.signature.data
        db.session.add(g.user)
        db.session.commit()
        flash('设置已保存')
        return redirect(url_for('.settings'))
    return render_template('account/settings/settings.html', form=form)


    # @bp.route('/resend_activate_mail')
    # @UserPermission()
    # def resend_activate_mail():
    # try:
    # signup_mail(g.user)
    # except Exception:
    # flash('邮件发送失败，请稍后尝试')
    #     else:
    #         flash('激活邮件已发送到你的邮箱，请查收')
    #     return redirect(url_for('.settings'))
