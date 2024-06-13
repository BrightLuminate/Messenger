from flask import Flask,request,redirect,url_for,jsonify
from myapp.views import myapp
from myapp.models import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messenger.db'
    db.init_app(app)
    app.register_blueprint(myapp, url_prefix="/myapp")

    @app.route('/')
    def root():
        return redirect(url_for('myapp.index'))

    @app.route('/signup', methods=['POST'])
    def signup():
        data = request.json
        username = data.get('username')
        password = data.get('password')

        print(f"회원가입 요청 받음 - 사용자 이름: {username}, 비밀번호: {password}")
        return jsonify({'message': '회원가입 성공'}), 200

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
