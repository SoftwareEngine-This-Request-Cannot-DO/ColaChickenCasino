from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
import CreditCard

money_bp = Blueprint('money', __name__)

@money_bp.route('/depositMoreChips')
@login_required
def depositMoreCoins():
    return render_template('chips.html', user=current_user, type="")

@money_bp.route('/depositWith/<type>', methods=['POST'])
@login_required
def creditCards(type):
    return render_template('chips.html', user=current_user, type=type)

'''
原本換籌碼方式：信用卡餘額＞代幣＞籌碼
更改後方式：信用卡餘額＞籌碼

備注：原本前端傳後端的方式用 ajax，現在改用 form
'''
@money_bp.route('/addChips',  methods=['POST'])
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