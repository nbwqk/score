from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_wtf import CSRFProtect

from apps.score.model import *
from apps.user.model import *
from apps import create_app
from exts import db

app = create_app()
manager=Manager(app=app)
migrate=Migrate(app=app,db=db)
csrf=CSRFProtect(app=app)
manager.add_command('db',MigrateCommand)


if __name__ == '__main__':
    manager.run()

