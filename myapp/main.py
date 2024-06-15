from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_socketio import join_room, leave_room, send
from flask_mail import Message
from .models import db, User
from .config import mail
from . import socketio
from flask import Flask, render_template, abort
myapp = Blueprint('myapp', __name__)

users = {
    "user1": {"username": "User1", "profile_image_url": "url_to_image1"},
    "user2": {"username": "User2", "profile_image_url": "url_to_image2"}
}

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

        temp_password = 'temporarypassword'
        user.set_password(temp_password)
        db.session.commit()

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
    friends = [
        {"id": "user1", "username": "User1", "profile_image_url": url_for('static', filename='puppy.jpg'), "last_message_time": "2분 전", "online": True},
        {"id": "user2", "username": "User2", "profile_image_url": url_for('static', filename='budg.jpg'), "last_message_time": "5분 전", "online": False},
    ]
    return render_template('people.html', friends=friends)

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
@myapp.route('/chat/<friend_id>')
def chat(friend_id):
    user = users().get(friend_id)  # 함수 호출을 추가
    if not user:
        abort(404, description="User not found")
    return render_template('chat.html', user=user)

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(f"{username} has entered the room.", room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(f"{username} has left the room.", room=room)

@socketio.on('message')
def handle_message(data):
    send(data, room=data['room'])

