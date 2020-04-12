# IMPORT STATEMENTS

from flask            import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_migrate    import Migrate

from flask_login      import LoginManager

from config           import Config

# INITIALIZATION/CONFIGURATION STATEMENTS

# "flask" is a framework
# "Flask" is a Python class datatype

# app = Flask(__name__) creates and instance
#  of the Flask class for the Healthcrypt application

app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

login_manager = LoginManager(app)

login_manager.login_view = 'login'

# FINAL IMPORT STATEMENT (this time, developer code)

from app import routes, models