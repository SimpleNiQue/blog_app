import os

from flask import Flask
from . import models, auth, blog

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    # Initialise Database Here
    models.init_app(app)

    # Register Blueprint here
    app.register_blueprint(auth.bp) # auth bluprint
    app.register_blueprint(blog.bp) # blog blueprint

    app.add_url_rule('/', endpoint='index')

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(
        app.instance_path, 'app.sqlite',
        )
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)

    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    @app.route('/hello', methods=('GET',))
    def hello():
        return "Hello, World!"
    
    return app

