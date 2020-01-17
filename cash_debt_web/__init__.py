from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database_v1.db'
app.config["SECRET_KEY"] = "OCML3BRawWEUeaxcuKHLpw"

db = SQLAlchemy(app)

import cash_debt_web.models
import cash_debt_web.routes