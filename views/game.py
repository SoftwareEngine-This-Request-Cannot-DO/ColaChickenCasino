from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
import subprocess, handler

game_bp = Blueprint('game', __name__)

@game_bp.route('/game/<gameType>')
@login_required
def game(gameType):
    if gameType == 'reel' and current_user.info['gameT']['reel'] == 0:
        current_user.info['chips'] += 500
        users = handler.get_users_data()
        users[current_user.account]['chips'] += 500
    return render_template(f'/games/{gameType}.html', user=current_user)

@game_bp.route('/slotrun', methods=['POST'])
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
    
@game_bp.route('/runblackjack', methods=['POST'])
@login_required
def runblackjack():
    data = request.form
    if len(data.get('chips-input')) > 0:
        chips = int(data.get('chips-input'))
    else:
        return f"<script>alert('籌碼不能為空');history.back();</script>"
    
    blackjack_script_path = './BlackJack21.py'
    subprocess.run(['python', blackjack_script_path, '--username', f'{current_user.account}'])
