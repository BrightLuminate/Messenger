from flask import Blueprint

myapp = Blueprint('myapp', __name__, template_folder='templates', static_folder='static')

from . import views
