from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models import Cliente
from app.forms import ClienteForm
from . import clientes_bp

@clientes_bp.route('/')
@clientes_bp.route('/listar')
@login_required
def listar():
    clientes = Cliente.query.all()
    return render_template('clientes/listar.html', clientes=clientes)

@clientes_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    form = ClienteForm()
    if form.validate_on_submit():
        cliente = Cliente(
            nombre=form.nombre.data,
            email=form.email.data,
            telefono=form.telefono.data,
            direccion=form.direccion.data,
            documento=form.documento.data
        )
        db.session.add(cliente)
        db.session.commit()
        flash('Cliente creado exitosamente', 'success')
        return redirect(url_for('clientes.listar'))
    return render_template('clientes/form.html', form=form, titulo='Nuevo Cliente')

@clientes_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    cliente = Cliente.query.get_or_404(id)
    form = ClienteForm(obj=cliente)
    if form.validate_on_submit():
        cliente.nombre = form.nombre.data
        cliente.email = form.email.data
        cliente.telefono = form.telefono.data
        cliente.direccion = form.direccion.data
        cliente.documento = form.documento.data
        db.session.commit()
        flash('Cliente actualizado exitosamente', 'success')
        return redirect(url_for('clientes.listar'))
    return render_template('clientes/form.html', form=form, titulo='Editar Cliente')

@clientes_bp.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    flash('Cliente eliminado exitosamente', 'success')
    return redirect(url_for('clientes.listar'))