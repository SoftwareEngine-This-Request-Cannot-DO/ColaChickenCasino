import json

def read_json_file(filename):
    try:
        with open(f"static/json/{filename}", "r", encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return None

def write_json_file(filename, new_data):
    try:
        with open(f"static/json/{filename}", 'w', encoding='utf-8') as f:
            json.dump(new_data, f, indent=2, ensure_ascii=False)
    except FileExistsError:
        return FileExistsError

def get_users_data():
    users = read_json_file('user.json')
    return users

def update_users_data(data):
    write_json_file('user.json', data)

def get_cards_data():
    cards = read_json_file('card.json')
    return cards

def update_cards_data(data):
    write_json_file('card.json', data)