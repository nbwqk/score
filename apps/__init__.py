from flask import Flask, render_template

from apps.score.view import score_bp
from apps.user.view import user_bp
from exts import db, login_manager
from settings import DevelopmentConfig

def page_not_found(e):
    return render_template('error/404.html'),404

def internal_server_error(e):
    return render_template('error/500.html'),500

def create_app():
    app=Flask(__name__,static_folder='../static',template_folder='../templates')
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    login_manager.init_app(app)
    app.register_blueprint(score_bp)
    app.register_blueprint(user_bp)
    app.register_error_handler(404,page_not_found)
    app.register_error_handler(500,internal_server_error)
    return app