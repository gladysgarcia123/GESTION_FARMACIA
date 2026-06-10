from flask import Blueprint

medicamentos_bp = Blueprint('medicamentos', __name__)

from . import routes