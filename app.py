from flask import Flask, Blueprint
import logging.config
import settings
from database import db
from core.blog.endpoints.posts import ns as blog_posts_namespace
from core.blog.endpoints.categories import ns as blog_categories_namespace
from core.restplus import api


def create_app():
    app = Flask(__name__)
    app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP

    db.app = app
    db.init_app(app)
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(blog_posts_namespace)
    api.add_namespace(blog_categories_namespace)
    app.register_blueprint(blueprint)

    # db.drop_all(app=app)
    # db.create_all(app=app)
    return app

def main():
    app = create_app()
    logging.config.fileConfig('logging.conf')
    log = logging.getLogger(__name__)
    log.info('>>>>> Starting development server at http://{}/api <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)

if __name__ == '__main__':
    main()
