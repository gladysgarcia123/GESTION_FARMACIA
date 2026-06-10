from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models import Proveedor
from app.forms import ProveedorForm
from . import proveedores_bp

@proveedores_bp.route('/')
@proveedores_bp.route('/listar')
@login_required
def listar():
    proveedores = Proveedor.query.all()
    return render_template('proveedores/listar.html', proveedores=proveedores)

@proveedores_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    form = ProveedorForm()
    if form.validate_on_submit():
        proveedor = Proveedor(
            nombre=form.nombre.data,
            contacto=form.contacto.data,
            telefono=form.telefono.data,
            email=form.email.data,
            direccion=form.direccion.data
        )
        db.session.add(proveedor)
        db.session.commit()
        flash('Proveedor creado exitosamente', 'success')
        return redirect(url_for('proveedores.listar'))
    return render_template('proveedores/form.html', form=form, titulo='Nuevo Proveedor')

@proveedores_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    proveedor = Proveedor.query.get_or_404(id)
    form = ProveedorForm(obj=proveedor)
    if form.validate_on_submit():
        proveedor.nombre = form.nombre.data
        proveedor.contacto = form.contacto.data
        proveedor.telefono = form.telefono.data
        proveedor.email = form.email.data
        proveedor.direccion = form.direccion.data
        db.session.commit()
        flash('Proveedor actualizado exitosamente', 'success')
        return redirect(url_for('proveedores.listar'))
    return render_template('proveedores/form.html', form=form, titulo='Editar Proveedor')

@proveedores_bp.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    proveedor = Proveedor.query.get_or_404(id)
    db.session.delete(proveedor)
    db.session.commit()
    flash('Proveedor eliminado exitosamente', 'success')
    return redirect(url_for('proveedores.listar'))