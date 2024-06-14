from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from .models import db, User
from flask_mail import Message
from . import mail

myapp = Blueprint('myapp', __name__)

@myapp.route('/')
def index():
    return render_template('index.html')

@myapp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['new_username']
        password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']

        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('myapp.signup'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists!')
            return redirect(url_for('myapp.signup'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': '회원가입이 완료되었습니다.'})

    return render_template('signup.html')

@myapp.route('/reset', methods=['GET', 'POST'])
def reset():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        email = data.get('email')

        user = User.query.filter_by(username=username, email=email).first()
        if not user:
            return jsonify({'error': 'Invalid username or email'}), 400

        # 임시 비밀번호 생성
        temp_password = 'temporarypassword'  # 실제로는 더 복잡한 비밀번호 생성 로직이 필요합니다.
        user.set_password(temp_password)
        db.session.commit()

        # 이메일 전송
        msg = Message('비밀번호 재설정', sender='your_email@gmail.com', recipients=[email])
        msg.body = f'안녕하세요, {username}님. 임시 비밀번호는 {temp_password} 입니다.'
        mail.send(msg)

        return jsonify({'message': '비밀번호 재설정 이메일이 전송되었습니다.'})

    return render_template('reset.html')

@myapp.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        return redirect(url_for('myapp.people'))
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@myapp.route('/people')
def people():
    return render_template('people.html')

@myapp.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@myapp.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!')
    else:
        flash('User not found!')
    return redirect(url_for('myapp.users'))

