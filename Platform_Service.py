import os
import re
from flask import Flask
from flask import redirect, request, views
from flask import Response
from flask import jsonify
import flask

from Blockchain_Platform import *

def create_app():
    
    app = Flask(__name__) #create the application instance
    app.config.from_object(__name__) #load onfig from this file
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    templates_dir = os.path.join(os.path.basename(os.getcwd()), 'templates')
    #load default config and override config from an enviroment variable
    app.add_url_rule('/blockchain_platform',
                        view_func=blockchain_platform.as_view('%s/%s' % (templates_dir, 'index')),
                         methods=["GET", "POST"])
    app.secret_key = "aaw"
    return app

if __name__ == "__main__":
    _port = 8000
    print('\n [*] Start API Service on port: %s' % (_port))
    app = create_app()
    app.run(host='0.0.0.0', port=_port, threaded=True, debug=True, use_reloader=True)
