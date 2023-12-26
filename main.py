from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask import Flask, flash, redirect, render_template, request, url_for, jsonify
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

with open('static/json/user.json', 'r', encoding='utf-8') as f:
    users = json.load(f)

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

@app.route('/game/<gameType>')
@login_required
def game(gameType):
    return render_template(f'/games/{gameType}.html', user=current_user)

@app.route('/slotrun', methods=['POST'])
def slotrun():
    try:
        data = request.get_json()
        print(data)
        chips_result = int(data['current']) - int(data['pay'])
        if data['result'] != '--':
            chips_result += int(data['result'])
        users[current_user.account]['chips'] = chips_result
        with open('static/json/user.json', 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
        return jsonify({'chips': chips_result})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/chat')
@login_required
def chat():
    return render_template('chat/chat.html', user=current_user)

@socketio.on('send_message')
def handle_message(data):
    print('Received message: ' + data['message'])  # print接收到的消息
    socketio.emit('receive_message', data)  # 廣播消息
    print('Message sent back to client')  # 確認訊息發送

@app.route('/depositMoreCoins')
@login_required
def depositMoreCoins():
    return render_template('money/coins.html', user=current_user, type="")

@app.route('/depositWith/<type>', methods=['POST'])
@login_required
def creditCards(type):
    return render_template('money/coins.html', user=current_user, type=type)

@app.route('/changeMoreChips',  methods=['POST'])
@login_required
def changeMoreChips():
    try:
        data = request.get_json()
        coins_result = int(data['coins']) - int(data['input_chips']) * 5
        chips_result = int(data['current_chips']) + int(data['input_chips'])
        users[current_user.account]['coin'] = coins_result
        users[current_user.account]['chips'] = chips_result
        with open('static/json/user.json', 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
        return jsonify({
                'coins': coins_result,
                'chips': chips_result
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)