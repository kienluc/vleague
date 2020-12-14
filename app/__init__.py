from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager
app = Flask(__name__)

app.secret_key = "sdsdqwgfdgrtrt"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@localhost:3306/vleague?charset?utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)
admin = Admin(app=app, name="Giải vô địch bóng đá quốc gia V-League", template_mode="bootstrap4")
login = LoginManager(app=app)
