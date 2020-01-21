from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database_v1.db'
app.config["SECRET_KEY"] = "OCML3BRawWEUeaxcuKHLpw"

db = SQLAlchemy(app)
login_manager = LoginManager(app=app)

import cash_debt_web.models
import cash_debt_web.routes