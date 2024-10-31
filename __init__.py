from flask import Blueprint

project1_bp = Blueprint('project1', __name__, template_folder='templates')

from . import routes
