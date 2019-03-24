from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

myFlaskApp = Flask(__name__)

myFlaskApp.config['SECRET_KEY'] = '1a43569a2beb6e6037101c071e091a96'

myFlaskApp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(myFlaskApp)

bcrypt = Bcrypt(myFlaskApp)

login_manager = LoginManager(myFlaskApp)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

myFlaskApp.config['MAIL_SERVER'] = 'smtp.googlemail.com'
myFlaskApp.config['MAIL_POST'] = 578
myFlaskApp.config['MAIL_USE_TLS'] = True
myFlaskApp.config['MAIL_USERNAME'] = 'ajesh.sit@gmail.com'
myFlaskApp.config['MAIL_PASSWORD'] = 'June@2011'
mail = Mail(myFlaskApp)



from myFlaskApplication import routes
