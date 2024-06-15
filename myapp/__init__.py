from flask import Flask
from .config import Config, mail
from .models import db
from flask_socketio import SocketIO

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SERVER_NAME'] = 'localhost:5000'
    app.config['APPLICATION_ROOT'] = '/'
    app.config['PREFERRED_URL_SCHEME'] = 'http'

    db.init_app(app)
    mail.init_app(app)
    socketio.init_app(app)
    
    from .main import myapp
    app.register_blueprint(myapp)
    
    with app.app_context():
        db.create_all()

    # users 딕셔너리를 설정합니다.
    app.config['users'] = {
        "user1": {
            "username": "User1",
            "profile_image_url": "/static/puppy.jpg"
        },
        "user2": {
            "username": "User2",
            "profile_image_url": "/static/budg.jpg"
        }
    }

    from .main import myapp
    app.register_blueprint(myapp)

    return app