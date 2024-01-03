from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask import Flask, flash, redirect, render_template, request, url_for, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import os, handler, CreditCard, subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = str(os.urandom(16).hex())
cors = CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

# app.register_blueprint(app)
# app.register_blueprint(app)

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

#/chat
@app.route('/getFriends')
@login_required
def getFriend():
    data = {'friends': current_user.info['friends']}
    return jsonify(data)

@app.route('/getAllUser')
@login_required
def getAllUser():
    data = {'users': []}
    for key, user in users.items():
        if key != current_user.account and user['username'] not in current_user.info['friends']:
            data['users'].append(user['username'])
    return jsonify(data)

@app.route('/addFriends', methods=['POST'])
@login_required
def addFriends():
    data = request.get_json()
    print(data)
    usersname = [user['username'] for key, user in users.items()]
    if data['username'] in usersname:
        users[current_user.account]['friends'].append(data['username'])
        handler.write_json_file('/user.json', users)
    data = {'friends': current_user.info['friends']}
    return jsonify(data)

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

@app.route('/depositMoreChips')
@login_required
def depositMoreCoins():
    users = handler.get_users_data()
    current_user.info['chips'] = users[current_user.account]['chips']
    return render_template('chips.html', user=current_user, type="")

@app.route('/depositWith/<type>', methods=['POST'])
@login_required
def creditCards(type):
    return render_template('chips.html', user=current_user, type=type)

'''
原本換籌碼方式：信用卡餘額＞代幣＞籌碼
更改後方式：信用卡餘額＞籌碼

備注：原本前端傳後端的方式用 ajax，現在改用 form
'''
@app.route('/addChips',  methods=['POST'])
@login_required
def changeMoreChips():
    try:
        data = request.form
        if len(data.get('deposit-money')) > 0:
            chips = int(data.get('deposit-money'))
        else:
            return f"<script>alert('籌碼不能為空');history.back();</script>"
        res = cardhandler(data, chips)
        if res[0]:
            current_user.info['chips'] += chips
            return render_template('chips.html', user=current_user, type='creditCard')
        return f"<script>alert('{res[1]}');history.back();</script>"
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def cardhandler(data, amount):
    card_data = {
        'cardNumber':[str(data.get('credit-number' + str(i))) for i in range(1, 5)],
        'cardDated': str(data.get('credit-dated')),
        'cardSecret': str(data.get('credit-secret'))
    }
    
    id = ''.join(card_data.get('cardNumber'))
    res = CreditCard.top_up_to_game(current_user.account, id, card_data.get("cardSecret"), card_data.get("cardDated"), amount)
    return [1, res] if "Success" in res else [0, res]

@app.route('/game/<gameType>')
@login_required
def game(gameType):
    users = handler.get_users_data()
    current_user.info['chips'] = users[current_user.account]['chips']
    if gameType == 'reel' and current_user.info['gameT']['reel'] == 0:
        current_user.info['chips'] += 500
        users = handler.get_users_data()
        users[current_user.account]['chips'] += 500
    return render_template(f'/games/{gameType}.html', user=current_user)

@app.route('/slotrun', methods=['POST'])
@login_required
def slotrun():
    try:
        data = request.get_json()
        chips_result = int(data['current']) - int(data['pay'])
        if data['result'] != '--':
            chips_result += int(data['result'])
        users = handler.get_users_data()
        users[current_user.account]['chips'] = chips_result
        users[current_user.account]['gameT']['reel'] += 1
        current_user.info['chips'] = chips_result
        current_user.info['gameT']['reel'] += 1
        handler.write_json_file('user.json', users)
        return jsonify({
                'chips': users[current_user.account]['chips'],
                'gameT': users[current_user.account]['gameT']['reel']
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/runblackjack', methods=['POST'])
@login_required
def runblackjack():
    data = request.form
    if len(data.get('chips-input')) > 0:
        chips = int(data.get('chips-input'))
    else:
        return f"<script>alert('籌碼不能為空');history.back();</script>"
    
    blackjack_script_path = './BlackJack21.py'
    subprocess.run(['python', blackjack_script_path, '--username', f'{current_user.account}'])


if __name__ == "__main__":
    users = handler.get_users_data()
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)