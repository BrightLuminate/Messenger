from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
import os
from dotenv import load_dotenv

# Create instances of extensions
db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # 이메일 설정 추가
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    # Setup login manager
    login_manager.login_view = 'myapp.login'
    login_manager.login_message = '로그인이 필요합니다.'

    from .views import myapp
    app.register_blueprint(myapp)

    with app.app_context():
        db.create_all()

    return app

@login_manager.user_loader
def load_user(user_id):
    from .models import User  # Prevent circular imports
    return User.query.get(int(user_id))