from flask import Blueprint

index_blueprint = Blueprint('index', __name__)


@index_blueprint.route('/')
def index_view():
    return 'Welcome! Server alive.'

