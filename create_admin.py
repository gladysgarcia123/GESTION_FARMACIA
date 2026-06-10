from app import create_app, db
from app.models import Usuario, Rol
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    print("Creando tablas...")
    db.create_all()
    
    # Crear roles
    print("Creando roles...")
    admin_role = Rol.query.filter_by(nombre='Admin').first()
    if not admin_role:
        admin_role = Rol(nombre='Admin')
        db.session.add(admin_role)
        print("✓ Rol Admin creado")
    else:
        print("✓ Rol Admin ya existe")
    
    vendedor_role = Rol.query.filter_by(nombre='Vendedor').first()
    if not vendedor_role:
        vendedor_role = Rol(nombre='Vendedor')
        db.session.add(vendedor_role)
        print("✓ Rol Vendedor creado")
    else:
        print("✓ Rol Vendedor ya existe")
    
    db.session.commit()
    
    # Crear usuario admin
    admin = Usuario.query.filter_by(username='admin').first()
    if not admin:
        admin = Usuario(
            username='admin',
            password=generate_password_hash('admin123'),
            rol_id=admin_role.id,
            nombre_completo='Administrador del Sistema',
            email='admin@farmacia.com'
        )
        db.session.add(admin)
        db.session.commit()
        print("✓ Usuario admin creado: admin / admin123")
    else:
        print("✓ Usuario admin ya existe")
    
    # Verificar que hay roles
    roles = Rol.query.all()
    print(f"\n📋 Roles disponibles: {[(r.id, r.nombre) for r in roles]}")
    
    print("\n✅ Configuración completada!")