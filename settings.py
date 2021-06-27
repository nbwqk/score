import os


class Config:
    DEBUG=True
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:''@127.0.0.1:3306/score_db'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_ECHO=True
    SECRET_KEY='nrwt34@#$%kh34tgf'
    # 项目路径
    BASE_DIR=os.path.dirname(os.path.abspath(__file__))
    # 静态文件夹的路径
    STATIC_DIR=os.path.join(BASE_DIR,'static')
    TEMPLATE_DIR=os.path.join(BASE_DIR,'template')
    UPLOAD_FILE_DIR=os.path.join(STATIC_DIR,'upload')

    PER_PAGE=3

class DevelopmentConfig(Config):
    ENV = 'development'

class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False