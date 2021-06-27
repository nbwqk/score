from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()
login_manager=LoginManager()
login_manager.login_view='user.login'
login_manager.login_message='请先登录！'