from flask import render_template
from flask_login import login_required, current_user
from app import db
from app.models import Venta, Medicamento, Cliente, Usuario
from . import admin_bp

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    total_ventas = Venta.query.count()
    total_medicamentos = Medicamento.query.count()
    total_clientes = Cliente.query.count()
    total_usuarios = Usuario.query.count()
    
    ingresos_totales = db.session.query(db.func.sum(Venta.total)).scalar() or 0
    
    stock_bajo = Medicamento.query.filter(Medicamento.stock <= Medicamento.stock_minimo).count()
    
    ventas_recientes = Venta.query.order_by(Venta.fecha.desc()).limit(5).all()
    
    medicamentos_stock_bajo = Medicamento.query.filter(Medicamento.stock <= Medicamento.stock_minimo).limit(5).all()
    
    return render_template('dashboard.html',
                         total_ventas=total_ventas,
                         total_medicamentos=total_medicamentos,
                         total_clientes=total_clientes,
                         total_usuarios=total_usuarios,
                         ingresos_totales=ingresos_totales,
                         stock_bajo=stock_bajo,
                         ventas_recientes=ventas_recientes,
                         medicamentos_stock_bajo=medicamentos_stock_bajo)