# coding: utf-8
from flask import Blueprint, render_template, url_for, redirect, request, json
from ..utils.permissions import AdminPermission
from ..models import db, Collection, CollectionKind, Work, CollectionWork
from ..forms import CollectionForm
from ..utils.decorators import jsonify

bp = Blueprint('collection', __name__)


@bp.route('/collection/add', methods=['GET', 'POST'])
@AdminPermission()
def add():
    """添加选集"""
    form = CollectionForm()
    form.kind_id.choices = [(c.id, c.name) for c in CollectionKind.query.order_by(CollectionKind.order.asc())]
    if form.validate_on_submit():
        collection = Collection(**form.data)
        collection_kind = CollectionKind.query.get_or_404(form.kind_id.data)
        collection.order = collection_kind.max_collection_order + 1
        collection.populate_tr_fields()
        db.session.add(collection)
        db.session.commit()
        return redirect(url_for('admin.collection_works', uid=collection.id))
    return render_template('collection/add/add.html', form=form)


@bp.route('/collection/<int:uid>/edit', methods=['GET', 'POST'])
@AdminPermission()
def edit(uid):
    """编辑选集"""
    collection = Collection.query.get_or_404(uid)
    form = CollectionForm(obj=collection)
    form.kind_id.choices = [(c.id, c.name) for c in CollectionKind.query.order_by(CollectionKind.order.asc())]
    if form.validate_on_submit():
        if collection.kind_id != form.kind_id.data:
            collection_kind = CollectionKind.query.get_or_404(form.kind_id.data)
            collection.order = collection_kind.max_collection_order + 1
        form.populate_obj(collection)
        collection.populate_tr_fields()
        db.session.add(collection)
        db.session.commit()
        return redirect(url_for('admin.collections'))
    return render_template('collection/edit/edit.html', form=form)


@bp.route('/collection/<int:uid>')
def view(uid):
    """选集"""
    collection = Collection.query.get_or_404(uid)
    return render_template('collection/view/view.html', collection=collection)


@bp.route('/collections')
def collections():
    """全部选集"""
    collection_kinds = CollectionKind.query.order_by(CollectionKind.order.asc())
    return render_template('collection/collections/collections.html', collection_kinds=collection_kinds)


@bp.route('/collection/<int:uid>/add_work')
@AdminPermission()
def add_work(uid):
    collection = Collection.query.get_or_404(uid)
    return render_template('collection/add_work/add_work.html', collection=collection)


@bp.route('/collection/<int:uid>/do_add_work', methods=['POST'])
@AdminPermission()
@jsonify
def do_add_work(uid):
    collection = Collection.query.get_or_404(uid)
    work_id = request.form.get('work_id', type=int)
    if not work_id:
        return {'result': False}
    work = Work.query.get_or_404(work_id)
    collection_work = CollectionWork.query.filter(CollectionWork.collection_id == uid,
                                                  CollectionWork.work_id == work_id).first()
    if collection_work:
        return {'result': True}
    collection_work = CollectionWork(collection_id=uid, work_id=work_id, order=collection.max_work_order + 1)
    db.session.add(collection_work)
    db.session.commit()
    return {'result': True}


@bp.route('/collection/update_works_order', methods=['POST'])
@AdminPermission()
@jsonify
def update_works_order():
    orders = request.form.get('orders')
    if not orders:
        return {'result': False}
    orders = json.loads(orders)
    for item in orders:
        id = item['id']
        order = item['order']
        collection_work = CollectionWork.query.get(id)
        if not collection_work:
            continue
        collection_work.order = order
        db.session.add(collection_work)
    db.session.commit()
    return {'result': True}


@bp.route('/collection/update_order', methods=['POST'])
@AdminPermission()
@jsonify
def update_order():
    orders = request.form.get('orders')
    if not orders:
        return {'result': False}
    orders = json.loads(orders)
    for item in orders:
        id = item['id']
        order = item['order']
        collection = Collection.query.get(id)
        if not collection:
            continue
        collection.order = order
        db.session.add(collection)
    db.session.commit()
    return {'result': True}


@bp.route('/admin/collection/<int:uid>/remove_work/<int:work_id>', methods=['POST'])
@AdminPermission()
@jsonify
def remove_work(uid, work_id):
    collection = Collection.query.get_or_404(uid)
    work = Work.query.get_or_404(work_id)
    collection_work = collection.works.filter(CollectionWork.work_id == work_id)
    map(db.session.delete, collection_work)
    db.session.commit()
    return {'result': True}
