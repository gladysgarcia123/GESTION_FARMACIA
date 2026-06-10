from flask import Blueprint

proveedores_bp = Blueprint('proveedores', __name__)

from . import routes