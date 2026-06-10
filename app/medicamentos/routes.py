from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.models import Medicamento, Proveedor, Categoria
from app.forms import MedicamentoForm
from . import medicamentos_bp

@medicamentos_bp.route('/')
@medicamentos_bp.route('/listar')
@login_required
def listar():
    medicamentos = Medicamento.query.all()
    return render_template('medicamentos/listar.html', medicamentos=medicamentos)

@medicamentos_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    form = MedicamentoForm()
    form.proveedor_id.choices = [(p.id, p.nombre) for p in Proveedor.query.all()]
    form.categoria_id.choices = [(c.id, c.nombre) for c in Categoria.query.all()]
    
    if form.validate_on_submit():
        medicamento = Medicamento(
            nombre=form.nombre.data,
            precio=form.precio.data,
            stock=form.stock.data,
            stock_minimo=form.stock_minimo.data,
            proveedor_id=form.proveedor_id.data,
            categoria_id=form.categoria_id.data
        )
        db.session.add(medicamento)
        db.session.commit()
        flash('Medicamento creado exitosamente', 'success')
        return redirect(url_for('medicamentos.listar'))
    
    return render_template('medicamentos/form.html', form=form, titulo='Nuevo Medicamento')

@medicamentos_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    medicamento = Medicamento.query.get_or_404(id)
    form = MedicamentoForm(obj=medicamento)
    form.proveedor_id.choices = [(p.id, p.nombre) for p in Proveedor.query.all()]
    form.categoria_id.choices = [(c.id, c.nombre) for c in Categoria.query.all()]
    
    if form.validate_on_submit():
        medicamento.nombre = form.nombre.data
        medicamento.precio = form.precio.data
        medicamento.stock = form.stock.data
        medicamento.stock_minimo = form.stock_minimo.data
        medicamento.proveedor_id = form.proveedor_id.data
        medicamento.categoria_id = form.categoria_id.data
        db.session.commit()
        flash('Medicamento actualizado exitosamente', 'success')
        return redirect(url_for('medicamentos.listar'))
    
    return render_template('medicamentos/form.html', form=form, titulo='Editar Medicamento')

@medicamentos_bp.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    medicamento = Medicamento.query.get_or_404(id)
    db.session.delete(medicamento)
    db.session.commit()
    flash('Medicamento eliminado exitosamente', 'success')
    return redirect(url_for('medicamentos.listar'))