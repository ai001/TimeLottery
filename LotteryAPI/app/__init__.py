# Import flask and template operators
from flask import Flask, render_template
from flask.ext.mail import Mail
from flask.ext.mongoengine import MongoEngine
from flask.ext.cache import Cache


# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Initialize cache
#cache = Cache()
#cache.init_app(app, config={ 'CACHE_TYPE': 'simple' })

# Define the database object which is imported
# by modules and controllers
db = MongoEngine()
db.connect(host=app.config['MONGODB_DATABASE_HOST'])
db.init_app(app)

# Define email
mail = Mail(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.auth.web.views import auth_web as auth_web_module
from app.auth.api.views import auth_api as auth_api_module
from app.admin.api.views import admin_api as admin_api_module
from app.ng_webui.views import ng_webui as ng_webui_module

# Register blueprint(s)
app.register_blueprint(auth_web_module)
app.register_blueprint(auth_api_module)
app.register_blueprint(admin_api_module)
app.register_blueprint(ng_webui_module)

