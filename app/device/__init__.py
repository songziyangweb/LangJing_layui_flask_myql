from flask import Blueprint

device = Blueprint('device',__name__)

from .device_views import *