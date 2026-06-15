from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config


db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar db con la app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Importar blueprints
    from app.auth.routes import auth_bp
    from app.admin.routes import admin_bp
    from app.medicamentos.routes import medicamentos_bp
    from app.ventas.routes import ventas_bp
    from app.proveedores.routes import proveedores_bp
    from app.clientes.routes import clientes_bp
   

    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(medicamentos_bp, url_prefix='/medicamentos')
    app.register_blueprint(ventas_bp, url_prefix='/ventas')
    app.register_blueprint(proveedores_bp, url_prefix='/proveedores')
    app.register_blueprint(clientes_bp, url_prefix='/clientes')


    return app

# Importar modelos después de crear db para evitar circular imports
from app import models

@login_manager.user_loader
def load_user(user_id):
    return models.Usuario.query.get(int(user_id))