from flask import Blueprint

monitor = Blueprint("monitor",__name__)

from .device_monitor_view import *