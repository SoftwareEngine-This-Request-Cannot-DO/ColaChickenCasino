from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask import Flask, flash, redirect, render_template, request, url_for, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from views.money import money_bp
from views.game import game_bp
import json, os, handler

app = Flask(__name__)
app.config['SECRET_KEY'] = str(os.urandom(16).hex())
cors = CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

app.register_blueprint(money_bp)
app.register_blueprint(game_bp)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.login_message = '這裡是充滿希望的地方，請表明你的身分'

class User(UserMixin):
    pass

user_statuses = {}  # 用於跟踪用戶狀態

@login_manager.user_loader
def user_loader(userid):
    if userid not in users:
        return

    user = User()
    user.id = users[userid]['username']
    user.account = userid
    user.info = {}
    for key, value in users[userid].items():
        if key != "username" and key != "password":
            user.info[key] = value
    return user


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    
    userid = request.form['user_id']
    if users != None:
        if (userid in users) and (request.form['password'] == users[userid]['password']):
            user = User()
            user.id = userid
            login_user(user)
            flash(f'{user}！ 歡迎來到可樂炸雞娛樂場！')
            return redirect(url_for('home'))
    flash('Login Failed...')
    return render_template('login.html')

@app.route('/logout')
def logout():
    user = current_user.get_id()
    logout_user()
    flash(f'{user}！歡迎下次再來！')
    return render_template('login.html')

@app.route('/home')
@login_required
def home():
    return render_template('home.html', user=current_user)

@app.route('/chat')
@login_required
def chat():
    return render_template('chat/chat.html', user=current_user)

@socketio.on('send_message')
def handle_message(data):
    print('Received message: ' + data['message'])
    print(data)
    username = data['user']  # 獲取當前用戶的用戶名
    message_data = {'message': data['message'], 'username': username}
    socketio.emit('receive_message', message_data)  # 廣播消息包含用戶名

@socketio.on('change_status')
def handle_status_change(data):
    status = data['status']
    print(f"Changing status for {data['user']} to {status}")  
    user_statuses[data['user']] = status  # 更新狀態

    # 廣播用戶狀態更改
    socketio.emit('status_updated', {'user': data['user'], 'status': status})

    # 廣播用戶上線或下線的消息
    status_message = f"{data['user']} {'上線' if status == 'online' else '下線'}"
    socketio.emit('receive_message', {'message': status_message, 'username': '系統'})

#/chat

if __name__ == "__main__":
    users = handler.get_users_data()
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)