from flask import Blueprint
records = Blueprint('records', __name__)
from app.records import routes