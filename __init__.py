from flask import Blueprint

project2_bp = Blueprint('project2', __name__, template_folder='templates')

from . import routes
