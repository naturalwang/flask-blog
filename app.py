from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from utils import log

from models import db
# import 具体的 Model 类, 给 migrate 用
from models.user import User
from models.blog import Blog
from models.weibo import Weibo, Comment
# from models.todo import Todo

app = Flask(__name__)
db_path = 'natural.sqlite'
manager = Manager(app)


def register_routes(app):
    # from routes.todo import main as routes_todo
    from routes.user import main as routes_user
    from routes.weibo import main as routes_weibo
    from routes.blog import main as routes_blog
    # from routes.api import main as routes_api

    # app.register_blueprint(routes_todo, url_prefix='/todo')
    app.register_blueprint(routes_user)
    app.register_blueprint(routes_weibo, url_prefix='/weibo')
    app.register_blueprint(routes_blog, url_prefix='/blog')
    # app.register_blueprint(routes_api, url_prefix='/api')


def configure_app():
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.secret_key = 'secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pwd@localhost/bbs'
    db.init_app(app)
    register_routes(app)


def configured_app():
    configure_app()
    return app


# 自定义的命令行命令用来运行服务器
@manager.command
def server():
    print('server run')
    # app = configured_app()
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=3000,
    )
    app.run(**config)


def configure_manager():
    """
    这个函数用来配置命令行选项
    """
    Migrate(app, db)
    manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    configure_manager()
    configure_app()
    manager.run()

# gunicorn -b '0.0.0.0:80' redischat:app
