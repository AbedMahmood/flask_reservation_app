import os, secrets
from flask import Flask
from config import Config
from datetime import datetime

app = Flask(__name__, static_url_path='/static')

default_secret_key = secrets.token_hex(8)
app.secret_key = os.getenv('SECRET_KEY', default_secret_key)
# First, define filters
@app.template_filter('format_date')
def format_date(value):
    if isinstance(value, datetime):
        return value.strftime('%m-%d-%Y')
    return value

@app.template_filter('format_time')
def format_time(time_str):
    time_obj = datetime.strptime(time_str, '%H:%M')
    return time_obj.strftime('%I:%M %p')

@app.template_filter('format_reservation_type')
def format_reservation_type(type_str):
    return ' '.join(word.capitalize() for word in type_str.split('_'))

app.config.from_object(Config)

@app.context_processor
def inject_nav_items():
    return dict(nav_items=Config.NAVIGATION_ITEMS)

from app.routes import index

app.jinja_env.filters['format_date'] = format_date
app.jinja_env.filters['format_time'] = format_time
app.jinja_env.filters['format_reservation_type'] = format_reservation_type

app.register_blueprint(index.bp)

