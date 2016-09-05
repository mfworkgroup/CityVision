import logging

from flask import Flask

from settings import Config
from extensions import oauth_service
from views.index import index_blueprint
from views.oauth import oauth_blueprint


LOGGER = logging.getLogger(__name__)


def create_app(config_file_env_var='SETTINGS_CONFIG'):
    app = Flask(__name__)
    # load default settings from Config
    app.config.from_object(Config)
    # load settings from file
    app.config.from_envvar(config_file_env_var)

    register_extentions(app)
    register_blueprint(app)

    return app


def register_extentions(app):
    oauth_service.init_app(app)


def register_blueprint(app):
    app.register_blueprint(index_blueprint)
    app.register_blueprint(oauth_blueprint)


application = create_app()

if __name__ == '__main__':
    application.run(debug=application.config['DEBUG'])
