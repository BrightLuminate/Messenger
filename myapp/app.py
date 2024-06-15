import os
from dotenv import load_dotenv
from myapp import create_app, socketio
from flask import Flask
from .models import db
from .main import myapp
from flask_mail import Mail, Message



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

mail = Mail(app)

db.init_app(app)
app.register_blueprint(myapp)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)