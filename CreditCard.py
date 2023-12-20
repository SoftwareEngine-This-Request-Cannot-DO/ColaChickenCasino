import json
from datetime import datetime

exchange_rate = 100

def read_json_file(filename):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return None

def write_json_file(filename, new_data):
    try:
        with open(filename, 'w') as f:
            json.dump(new_data, f, indent=2)
    except FileExistsError:
        return FileExistsError

def luhn_algorithm_optimized(card_number):
    card_number = [int(digit) for digit in str(card_number)][::-1]
    total = 0

    for i in range(len(card_number)):
        if i % 2 == 1:
            digit = card_number[i] * 2
            if digit > 9:
                digit -= 9
            total += digit
        else:
            total += card_number[i]

    return total % 10 == 0

# credit card generator
# https://saijogeorge.com/dummy-credit-card-generator/

def is_valid_card(card_number):
    sanitized_number = card_number.replace(" ", "")

    if sanitized_number.isdigit() and len(sanitized_number) == 16:
        return luhn_algorithm_optimized(sanitized_number)
    else:
        return False

def is_expiry(expiration_date, valid_from_date):
    expiration_date = datetime.strptime(expiration_date, "%m/%y")
    valid_from_date = datetime.strptime(valid_from_date, "%m/%y")
    current_date = datetime.today()

    if valid_from_date <= current_date <= expiration_date:
        return False
    else:
        return True
    
def verity(card_number):
    if is_valid_card(card_number):
        cards = read_json_file("card.json")
        card_info = cards.get(card_number, None)
        if card_info is not None and not is_expiry(card_info["Good Thru"], card_info["Valid From"]):
            return True
        else:
            return None
        
def top_up_to_game(player_name, card_number, amount):
    if verity(card_number):
        card_data = read_json_file("card.json")
        if card_data is not None and card_number in card_data:
            card_amount = card_data[card_number]["Amount"]
            if card_amount >= amount:
                card_amount -= amount
            else:
                return "Insufficient balance"
            
            card_data[card_number]["Amount"] = card_amount
            player_data = read_json_file("player.json")
            
            if player_name in player_data:
                player_data[player_name]["Amount"] += amount * exchange_rate
                write_json_file("card.json", card_data)
                write_json_file("player.json", player_data)

                msg = "Success top-up. \nPlayer's amount: " + str(player_data[player_name]["Amount"]) + "\nCard amount: " + str(card_amount)
                return msg
            else:
                return "Player not found in player.json"
        else:
            return "Card number not found in card.json"
    else:
        return "Invalid card number"

def top_up_to_card(player_name, card_number, amount):
    player_data = read_json_file("player.json")
    if player_name in player_data:
        player_amount = player_data[player_name]["Amount"]
        if verity(card_number):
            card_data = read_json_file("card.json")
            if card_data is not None and card_number in card_data:
                card_amount = card_data[card_number]["Amount"]
                if player_amount >= amount:
                    temp = amount / exchange_rate
                    player_amount -= amount
                    card_amount += temp
                else:
                    return "Insufficient balance"
                
                card_data[card_number]["Amount"] = int(card_amount)
                player_data[player_name]["Amount"] = player_amount
                write_json_file("card.json", card_data)
                write_json_file("player.json", player_data)

                msg = "Success top-up. \nPlayer's amount: " + str(player_data[player_name]["Amount"]) + "\nCard amount: " + str(card_amount)
                return msg
                
            else:
                return "Card number not found in card.json"
        else:
            return "Invalid card number"
    else:
        return "Player not found in player.json"

# testing
print(top_up_to_card("Player001", "4492150724110952", 10000))
print(top_up_to_game("Player001", "4492150724110952", 500))