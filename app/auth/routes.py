from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash  # ← security, NO secure
from app import db
from app.models import Usuario, Rol
from app.forms import LoginForm, RegisterForm
from . import auth_bp

# ==================== REGISTRO ====================
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    form = RegisterForm()
    
    # Cargar roles disponibles
    form.rol_id.choices = [(r.id, r.nombre) for r in Rol.query.all()]
    
    if form.validate_on_submit():
        # Verificar si el usuario ya existe
        existing_user = Usuario.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('El nombre de usuario ya existe', 'danger')
            return render_template('register.html', form=form)
        
        # Verificar email
        if form.email.data:
            existing_email = Usuario.query.filter_by(email=form.email.data).first()
            if existing_email:
                flash('El email ya está registrado', 'danger')
                return render_template('register.html', form=form)
        
        # Crear usuario
        hashed_password = generate_password_hash(form.password.data)
        user = Usuario(
            username=form.username.data,
            email=form.email.data,
            nombre_completo=form.nombre_completo.data,
            password=hashed_password,
            rol_id=form.rol_id.data
        )
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('¡Registro exitoso! Ahora puedes iniciar sesión', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar: {str(e)}', 'danger')
    
    return render_template('register.html', form=form)

# ==================== LOGIN ====================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'Bienvenido {user.username}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin.dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    
    return render_template('login.html', form=form)

# ==================== LOGOUT ====================
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('auth.login'))

# ==================== PERFIL ====================
@auth_bp.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html', usuario=current_user)