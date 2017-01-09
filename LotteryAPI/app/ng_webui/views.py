import os
from flask import Blueprint, render_template, url_for, send_from_directory
from config import WEB_UI_FOLDER
from app.utilities.common import nocache

ng_webui = Blueprint('ng_webui', __name__)


@ng_webui.route('/')
def ng_webui_home():
    return render_template('ng_webui/index.html')


# This is required by zone.js as it need to access the
# "main.js" file in the "ClientApp\app" folder which it
# does by accessing "<your-site-path>/app/main.js"
@ng_webui.route('/app/<path:filename>')
@nocache
def client_app_app_folder(filename):
    return send_from_directory(os.path.join(WEB_UI_FOLDER, "app"), filename)


# Custom static data
@ng_webui.route('/<path:filename>')
@nocache
def client_app_folder(filename):
    return send_from_directory(WEB_UI_FOLDER, filename)
