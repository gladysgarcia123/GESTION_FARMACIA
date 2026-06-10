from app import create_app, db
from app.models import Usuario, Rol, Cliente, Proveedor, Medicamento, Categoria, Venta, DetalleVenta

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'Usuario': Usuario, 
        'Rol': Rol,
        'Cliente': Cliente,
        'Proveedor': Proveedor,
        'Medicamento': Medicamento,
        'Categoria': Categoria,
        'Venta': Venta,
        'DetalleVenta': DetalleVenta
    }

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)