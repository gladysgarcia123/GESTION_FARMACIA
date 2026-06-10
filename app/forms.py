from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange, EqualTo, ValidationError  # ← Cambia ValidationResult por ValidationError

# ==================== FORMULARIO DE LOGIN ====================
class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

# ==================== FORMULARIO DE REGISTRO ====================
class RegisterForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired(), Length(min=4, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    nombre_completo = StringField('Nombre completo', validators=[DataRequired(), Length(max=150)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password', message='Las contraseñas deben coincidir')])
    rol_id = SelectField('Rol', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Registrarse')

# ==================== FORMULARIO DE MEDICAMENTOS ====================
class MedicamentoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    precio = FloatField('Precio', validators=[DataRequired(), NumberRange(min=0)])
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    stock_minimo = IntegerField('Stock Mínimo', validators=[DataRequired(), NumberRange(min=0)])
    proveedor_id = SelectField('Proveedor', coerce=int, validators=[DataRequired()])
    categoria_id = SelectField('Categoría', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Guardar')

# ==================== FORMULARIO DE CLIENTES ====================
class ClienteForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[Email()])
    telefono = StringField('Teléfono', validators=[Length(max=20)])
    direccion = StringField('Dirección', validators=[Length(max=200)])
    documento = StringField('Documento', validators=[Length(max=50)])
    submit = SubmitField('Guardar')

# ==================== FORMULARIO DE PROVEEDORES ====================
class ProveedorForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    contacto = StringField('Contacto', validators=[Length(max=100)])
    telefono = StringField('Teléfono', validators=[Length(max=20)])
    email = StringField('Email', validators=[Email()])
    direccion = StringField('Dirección', validators=[Length(max=200)])
    submit = SubmitField('Guardar')

# ==================== FORMULARIO DE VENTAS ====================
class VentaForm(FlaskForm):
    cliente_id = SelectField('Cliente', coerce=int, validators=[DataRequired()])
    medicamento_id = SelectField('Medicamento', coerce=int, validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Registrar Venta')