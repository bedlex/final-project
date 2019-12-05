from flask import Flask
from config import Config
from flask_mail import Mail


from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_login import LoginManager



app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)

db = SQLAlchemy(app)
migrate = Migrate(app,db)

# Login Flow config
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login" # This specifies what page to load for non-authoed users
#Mail


from app_base import routes, models
