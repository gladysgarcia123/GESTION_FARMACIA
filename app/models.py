from flask_login import UserMixin
from datetime import datetime

# NO definas db aquí, la vas a importar desde app
from app import db

class Rol(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    usuarios = db.relationship('Usuario', backref='rol', lazy=True)

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    email = db.Column(db.String(120))
    nombre_completo = db.Column(db.String(150))

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(200))
    documento = db.Column(db.String(50))
    ventas = db.relationship('Venta', backref='cliente', lazy=True)

class Proveedor(db.Model):
    __tablename__ = 'proveedores'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contacto = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100))
    direccion = db.Column(db.String(200))
    medicamentos = db.relationship('Medicamento', backref='proveedor', lazy=True)

class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.String(200))
    medicamentos = db.relationship('Medicamento', backref='categoria', lazy=True)

class Medicamento(db.Model):
    __tablename__ = 'medicamentos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    stock_minimo = db.Column(db.Integer, default=5)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'))
    fecha_vencimiento = db.Column(db.Date)
    detalles_venta = db.relationship('DetalleVenta', backref='medicamento', lazy=True)

class Venta(db.Model):
    __tablename__ = 'ventas'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    total = db.Column(db.Float, default=0)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    detalles = db.relationship('DetalleVenta', backref='venta', lazy=True, cascade='all, delete-orphan')

class DetalleVenta(db.Model):
    __tablename__ = 'detalles_venta'
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'), nullable=False)
    medicamento_id = db.Column(db.Integer, db.ForeignKey('medicamentos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)