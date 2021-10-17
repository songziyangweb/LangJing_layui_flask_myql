from flask import Blueprint

sys = Blueprint('sys',__name__)

from .sensor_views import *
from .user_views import *
