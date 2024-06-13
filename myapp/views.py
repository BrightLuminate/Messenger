from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, Message

myapp = Blueprint('myapp', __name__, template_folder='templates', static_folder='static')

@myapp.route('/')
def index():
    return render_template('index.html')

@myapp.route('/people', methods=['GET', 'POST'])
def people():
    return render_template('people.html')

@myapp.route('/new/signup', methods=['GET', 'POST'], endpoint='signup')
def signup():
    return render_template('signup.html')

@myapp.route('/new/reset', methods=['GET', 'POST'], endpoint='reset')
def reset():
    return render_template('reset.html')

@myapp.route('/friend_list')
def friend_list():
    friends = [{"id": 1, "name": "Buddy"}, {"id": 2, "name": "Charlie"}]
    return render_template('friend_list.html', friends=friends)

@myapp.route('/chat_list/<int:friend_id>')
def chat_list(friend_id):
    chats = [{"id": 1, "name": "Buddy"}, {"id": 2, "name": "Charlie"}]
    return render_template('chat_list.html', chats=chats, friend_id=friend_id)

@myapp.route('/chat_room/<int:chat_id>', methods=['GET', 'POST'])
def chat_room(chat_id):
    if request.method == 'POST':
        sender_id = request.form['sender_id']
        receiver_id = request.form['receiver_id']
        content = request.form['content']
        new_message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content)
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for('myapp.chat_room', chat_id=chat_id))

    messages = Message.query.filter_by(receiver_id=chat_id).all()
    return render_template('chat_room.html', messages=messages, chat_id=chat_id)
