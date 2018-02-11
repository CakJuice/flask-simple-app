from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_argon2 import Argon2
from flask_mail import Mail
from flask_login import LoginManager, current_user

from config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

argon2 = Argon2(app)
mail = Mail(app)

login_manager = LoginManager(app)
login_manager.login_view = 'base.login'

@app.before_request
def _before_request():
    """Auto call before page requested

    Decorators:
        app.before_request
    """

    g.user = current_user
