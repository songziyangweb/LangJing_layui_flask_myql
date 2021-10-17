from flask import Blueprint

his = Blueprint('his', __name__)

from .his_data_view import *
