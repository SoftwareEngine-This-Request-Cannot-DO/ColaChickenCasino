from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_socketio import SocketIO
from flask_cors import CORS
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = str(os.urandom(16).hex())
cors = CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.login_message = '這裡是充滿希望的地方，請表明你的身分'

class User(UserMixin):
    pass

with open('user.json', 'r', encoding='utf-8') as f:
    users = json.load(f)

@login_manager.user_loader
def user_loader(userid):
    if userid not in users:
        return

    user = User()
    user.id = users[userid]['username']
    return user


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    
    userid = request.form['user_id']
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

@app.route('/game')
@login_required
def game():
    return render_template('game.html', user=current_user)

@app.route('/chat')

@login_required
def chat():
    return render_template('chat.html', user=current_user)

@socketio.on('send_message')
def handle_message(data):
    print('Received message: ' + data['message'])  # print接收到的消息
    socketio.emit('receive_message', data)  # 廣播消息
    print('Message sent back to client')  # 確認訊息發送

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)