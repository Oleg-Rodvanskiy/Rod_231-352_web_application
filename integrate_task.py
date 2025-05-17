from flask import Flask, render_template, session, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Примеры данных
completed_contracts = [
    {'monster': 'Грифон', 'reward': 150},
    {'monster': 'Вампайр', 'reward': 200},
    {'monster': 'Медведь', 'reward': 100},
]

equipment = {
    'sword': 'Steel Sword',
    'silver_sword': 'Silver Sword',
    'armor': 'Witcher Armor',
}

active_quests = [
    'Уничтожить Грифона',
    'Спасти деревню от вампиров',
]

alchemy_items = [
    {'name': 'Черная кровь', 'type': 'potion', 'toxicity': 40},
    {'name': 'Золотая иволга', 'type': 'potion', 'toxicity': 5},
    {'name': 'Маска смерти', 'type': 'bomb', 'toxicity': 15},
]

@app.route('/initialize_session')
def initialize_session():
    session['toxicity'] = 20
    return "Сессия инициализирована!"

@app.route('/witcher/stats')
def witcher_stats():
    return render_template('witcher_stats.html', equipment=equipment, toxicity=session['toxicity'], active_quests=active_quests)

def calculate_total_gold(contracts):
    return sum(contract['reward'] for contract in contracts)

@app.route('/calculate_gold')
def calculate_gold():
    total_gold = calculate_total_gold(completed_contracts)
    return f'Общее количество золота: {total_gold}'

@app.route('/alchemy', methods=['GET'])
def alchemy():
    max_toxicity = request.args.get('toxicity', type=int)
    filtered_items = [item for item in alchemy_items if item['toxicity'] > max_toxicity]
    return jsonify(filtered_items)

if __name__ == '__main__':
    app.run(debug=True)