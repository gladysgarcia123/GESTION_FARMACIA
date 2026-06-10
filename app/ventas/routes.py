from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Venta, DetalleVenta, Medicamento, Cliente
from app.forms import VentaForm
from . import ventas_bp

@ventas_bp.route('/')
@ventas_bp.route('/listar')
@login_required
def listar():
    ventas = Venta.query.order_by(Venta.fecha.desc()).all()
    return render_template('ventas/listar.html', ventas=ventas)

@ventas_bp.route('/nueva', methods=['GET', 'POST'])
@login_required
def nueva():
    form = VentaForm()
    form.cliente_id.choices = [(0, 'Seleccione cliente...')] + [(c.id, c.nombre) for c in Cliente.query.all()]
    form.medicamento_id.choices = [(m.id, f"{m.nombre} - Stock: {m.stock} - ${m.precio}") for m in Medicamento.query.filter(Medicamento.stock > 0).all()]
    
    if request.method == 'POST' and form.validate_on_submit():
        venta = Venta(
            cliente_id=form.cliente_id.data if form.cliente_id.data != 0 else None,
            usuario_id=current_user.id,
            total=0
        )
        db.session.add(venta)
        db.session.commit()
        
        # Agregar detalle
        medicamento = Medicamento.query.get(form.medicamento_id.data)
        cantidad = form.cantidad.data
        subtotal = medicamento.precio * cantidad
        
        detalle = DetalleVenta(
            venta_id=venta.id,
            medicamento_id=medicamento.id,
            cantidad=cantidad,
            precio_unitario=medicamento.precio,
            subtotal=subtotal
        )
        db.session.add(detalle)
        
        # Actualizar stock
        medicamento.stock -= cantidad
        
        # Actualizar total de la venta
        venta.total = subtotal
        
        db.session.commit()
        
        flash('Venta registrada exitosamente', 'success')
        return redirect(url_for('ventas.listar'))
    
    return render_template('ventas/nueva.html', form=form)

@ventas_bp.route('/detalle/<int:id>')
@login_required
def detalle(id):
    venta = Venta.query.get_or_404(id)
    return render_template('ventas/detalle.html', venta=venta)

@ventas_bp.route('/buscar_medicamento')
@login_required
def buscar_medicamento():
    search = request.args.get('q', '')
    medicamentos = Medicamento.query.filter(
        Medicamento.nombre.contains(search),
        Medicamento.stock > 0
    ).limit(10).all()
    
    return jsonify([{
        'id': m.id,
        'nombre': m.nombre,
        'precio': m.precio,
        'stock': m.stock
    } for m in medicamentos])