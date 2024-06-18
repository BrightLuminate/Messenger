from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session, abort
from flask_socketio import join_room, leave_room, send
from flask_mail import Message
from .models import db, User
from .config import mail
from . import socketio

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
        session['user_id'] = user.id
        return redirect(url_for('myapp.people'))
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@myapp.route('/people')
def people():
    main_profile = {
        "username": "최도현",
        "link": "https://portfolio-laew.vercel.app/",
        "link_text": "https://portfolio-laew.vercel.app/ (프로필)",
        "profile_image_url": url_for('static', filename='jsj.jpeg'),
    }

    updated_profiles = [
        {"id": "진돗개", "username": "진돗개", "profile_image_url": url_for('static', filename='dog.jpg')},
        {"id": "시바 이누", "username": "시바 이누", "profile_image_url": url_for('static', filename='puppy.jpg')},
        {"id": "말티즈", "username": "말티즈", "profile_image_url": url_for('static', filename='do.jpg')},
        {"id": "푸들", "username": "푸들", "profile_image_url": url_for('static', filename='dogs.jpg')},
        {"id": "요크셔 테리어", "username": "요크셔 테리어", "profile_image_url": url_for('static', filename='sad.jpg')},
        {"id": "시추", "username": "시추", "profile_image_url": url_for('static', filename='animal-6852265_640.jpg')},
        {"id": "페키니즈", "username": "페키니즈", "profile_image_url": url_for('static', filename='pekingese-3823920_640.jpg')},
        {"id": "포메라니안", "username": "포메라니안", "profile_image_url": url_for('static', filename='pet-6718524_640.jpg')},
        {"id": "불독", "username": "불독", "profile_image_url": url_for('static', filename='bulldog-7476727_640.jpg')},
        {"id": "비숑 프리제", "username": "비숑 프리제", "profile_image_url": url_for('static', filename='bichon-6659330_640.jpg')},
        {"id": "치와와", "username": "치와와", "profile_image_url": url_for('static', filename='chihuahua-453063_640.jpg')},
        {"id": "골든 리트리버", "username": "골든 리트리버", "profile_image_url": url_for('static', filename='dog-7671355_640.jpg')},
        {"id": "래브라도 리트리버", "username": "래브라도 리트리버", "profile_image_url": url_for('static', filename='labrador-retriever-6158095_640.jpg')},
        {"id": "독일 셰퍼드", "username": "독일 셰퍼드", "profile_image_url": url_for('static', filename='german-shepherd-dog-2891659_640.jpg')},
        {"id": "로트와일러", "username": "로트와일러", "profile_image_url": url_for('static', filename='dog-3210211_640.jpg')},
        {"id": "도베르만", "username": "도베르만", "profile_image_url": url_for('static', filename='dog-1045298_640.jpg')},
        {"id": "허스키", "username": "허스키", "profile_image_url": url_for('static', filename='husky-2443664_640.jpg')},
        {"id": "웰시 코기", "username": "웰시 코기", "profile_image_url": url_for('static', filename='corgi-6705821_640.jpg')},
        {"id": "아키타", "username": "아키타", "profile_image_url": url_for('static', filename='akita-5964180_640.jpg')},
        {"id": "스피츠", "username": "스피츠", "profile_image_url": url_for('static', filename='dog-7850038_640.jpg')},
        {"id": "코커 스패니얼", "username": "코커 스패니얼", "profile_image_url": url_for('static', filename='cocker-spaniel-2130398_640.jpg')},
        {"id": "불 테리어", "username": "불 테리어", "profile_image_url": url_for('static', filename='dog-2421378_640.jpg')},
        {"id": "진돗개", "username": "진돗개", "profile_image_url": url_for('static', filename='dog.jpg')},
        {"id": "시바 이누", "username": "시바 이누", "profile_image_url": url_for('static', filename='puppy.jpg')},
        {"id": "말티즈", "username": "말티즈", "profile_image_url": url_for('static', filename='do.jpg')},
        {"id": "푸들", "username": "푸들", "profile_image_url": url_for('static', filename='dogs.jpg')},
        {"id": "불독", "username": "불독", "profile_image_url": url_for('static', filename='bulldog-7476727_640.jpg')},
        {"id": "비숑 프리제", "username": "비숑 프리제", "profile_image_url": url_for('static', filename='bichon-6659330_640.jpg')},
        {"id": "치와와", "username": "치와와", "profile_image_url": url_for('static', filename='chihuahua-453063_640.jpg')},
        {"id": "골든 리트리버", "username": "골든 리트리버", "profile_image_url": url_for('static', filename='dog-7671355_640.jpg')},
        {"id": "래브라도 리트리버", "username": "래브라도 리트리버", "profile_image_url": url_for('static', filename='labrador-retriever-6158095_640.jpg')},
        # 추가된 프로필 예시
    ]
    birthday_friends = [
        {"id": "프렌치 불독", "username": "프렌치 불독", "profile_image_url": url_for('static', filename='excited-5227932_640.jpg'), "last_message": "만나서 반가워요", "online": False},
       
        # 생일 친구 예시
    ]
    favorites = [
        {"id": "포메라니안", "username": "포메라니안", "profile_image_url": url_for('static', filename='pet-6718524_640.jpg'), "last_message_time": "10분 전", "online": True},
        {"id": "스피츠", "username": "스피츠", "profile_image_url": url_for('static', filename='dog-7850038_640.jpg'), "last_message_time": "10분 전", "online": True},
        {"id": "도베르만", "username": "도베르만", "profile_image_url": url_for('static', filename='dog-1045298_640.jpg'), "last_message_time": "10분 전", "online": True},
        # 즐겨찾기 예시
    ]
    friends = [
        {"id": "독일 셰퍼드", "username": "독일 셰퍼드", "profile_image_url": url_for('static', filename='german-shepherd-dog-2891659_640.jpg'), "last_message_time": "2시간 전", "online": True},
        {"id": "치와와", "username": "치와와", "profile_image_url": url_for('static', filename='chihuahua-453063_640.jpg'), "last_message_time": "3시간 전", "online": True},
        {"id": "말티즈", "username": "말티즈", "profile_image_url": url_for('static', filename='do.jpg'), "last_message_time": "1시간 전", "online": True},
        {"id": "진돗개", "username": "진돗개", "profile_image_url": url_for('static', filename='dog.jpg'), "last_message_time": "2시간 전", "online": True},
        {"id": "시바 이누", "username": "시바 이누", "profile_image_url": url_for('static', filename='puppy.jpg'), "last_message_time": "5시간 전", "online": True},
        {"id": "말티즈", "username": "말티즈", "profile_image_url": url_for('static', filename='do.jpg'), "last_message_time": "1시간 전", "online": True},
        {"id": "푸들", "username": "푸들", "profile_image_url": url_for('static', filename='dogs.jpg'), "last_message_time": "1시간 전", "online": True},
        {"id": "요크셔 테리어", "username": "요크셔 테리어", "profile_image_url": url_for('static', filename='sad.jpg'), "last_message_time": "1시간 전", "online": True},
        {"id": "시추", "username": "시추", "profile_image_url": url_for('static', filename='animal-6852265_640.jpg'), "last_message_time": "1시간 전", "online": True},
        {"id": "페키니즈", "username": "페키니즈", "profile_image_url": url_for('static', filename='pekingese-3823920_640.jpg'), "last_message_time": "1시간 전", "online": True},
        {"id": "포메라니안", "username": "포메라니안", "profile_image_url": url_for('static', filename='pet-6718524_640.jpg'), "last_message_time": "1시간 전", "online": True},
        {"id": "불독", "username": "불독", "profile_image_url": url_for('static', filename='bulldog-7476727_640.jpg'), "last_message_time": "1시간 전", "online": True},
        {"id": "비숑 프리제", "username": "비숑 프리제", "profile_image_url": url_for('static', filename='bichon-6659330_640.jpg'), "last_message_time": "1시간 전", "online": True},
        {"id": "치와와", "username": "치와와", "profile_image_url": url_for('static', filename='chihuahua-453063_640.jpg'), "last_message_time": "1시간 전", "online": True},
        {"id": "골든 리트리버", "username": "골든 리트리버", "profile_image_url": url_for('static', filename='dog-7671355_640.jpg'), "last_message_time": "1시간 전", "online": True},
        {"id": "래브라도 리트리버", "username": "래브라도 리트리버", "profile_image_url": url_for('static', filename='labrador-retriever-6158095_640.jpg'), "last_message_time": "1시간 전", "online": True},
    ]

    session['friends'] = friends + updated_profiles + birthday_friends + favorites  # 친구 목록 세션에 저장
    return render_template('people.html', main_profile=main_profile, updated_profiles=updated_profiles, birthday_friends=birthday_friends, favorites=favorites, friends=friends)

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
    user = next((friend for friend in session['friends'] if friend['id'] == friend_id), None)
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


@myapp.route('/rooms')
def rooms():
    friends = [
        {"id": "독일 셰퍼드", "username": "독일 셰퍼드", "profile_image_url": url_for('static', filename='german-shepherd-dog-2891659_640.jpg'), "last_message_time": "하이루", "online": True},
        {"id": "치와와", "username": "치와와", "profile_image_url": url_for('static', filename='chihuahua-453063_640.jpg'), "last_message_time": "🧗🏽‍♂️", "online": True},
        {"id": "말티즈", "username": "말티즈", "profile_image_url": url_for('static', filename='do.jpg'), "last_message_time": "🏵️", "online": True},
        {"id": "진돗개", "username": "진돗개", "profile_image_url": url_for('static', filename='dog.jpg'), "last_message_time": "🚣🏻", "online": True},
        {"id": "시바 이누", "username": "시바 이누", "profile_image_url": url_for('static', filename='puppy.jpg'), "last_message_time": "🎻", "online": True},
        {"id": "말티즈", "username": "말티즈", "profile_image_url": url_for('static', filename='do.jpg'), "last_message_time": "🎤", "online": True},
        {"id": "푸들", "username": "푸들", "profile_image_url": url_for('static', filename='dogs.jpg'), "last_message_time": "🎖️", "online": True},
        {"id": "요크셔 테리어", "username": "요크셔 테리어", "profile_image_url": url_for('static', filename='sad.jpg'), "last_message_time": "😎", "online": True},
        {"id": "시추", "username": "시추", "profile_image_url": url_for('static', filename='animal-6852265_640.jpg'), "last_message_time": "😅", "online": True},
        {"id": "페키니즈", "username": "페키니즈", "profile_image_url": url_for('static', filename='pekingese-3823920_640.jpg'), "last_message_time": "☮️", "online": True},
        {"id": "포메라니안", "username": "포메라니안", "profile_image_url": url_for('static', filename='pet-6718524_640.jpg'), "last_message_time": "🧡", "online": True},
        {"id": "불독", "username": "불독", "profile_image_url": url_for('static', filename='bulldog-7476727_640.jpg'), "last_message_time": "🥞", "online": True},
        {"id": "비숑 프리제", "username": "비숑 프리제", "profile_image_url": url_for('static', filename='bichon-6659330_640.jpg'), "last_message_time": "🍏", "online": True},
        {"id": "치와와", "username": "치와와", "profile_image_url": url_for('static', filename='chihuahua-453063_640.jpg'), "last_message_time": "🐦", "online": True},
        {"id": "골든 리트리버", "username": "골든 리트리버", "profile_image_url": url_for('static', filename='dog-7671355_640.jpg'), "last_message_time": "🐻", "online": True},
        {"id": "래브라도 리트리버", "username": "래브라도 리트리버", "profile_image_url": url_for('static', filename='labrador-retriever-6158095_640.jpg'), "last_message_time": "1시간 전", "online": True},
    ]
    session['friends'] = friends   # 친구 목록 세션에 저장
    return render_template('rooms.html',  friends=friends)


@myapp.route('/settings')
def settings():
    return render_template('settings.html')

@socketio.on('message')
def handle_message(data):
    send(data, room=data['room'])





