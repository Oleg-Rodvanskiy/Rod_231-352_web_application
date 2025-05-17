from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Мок-данные для алхимических предметов
alchemy_items = [
    {'name': 'Черная кровь', 'type': 'potion', 'toxicity': 10},
    {'name': 'Золотая иволга', 'type': 'potion', 'toxicity': 5},
    {'name': 'Маска смерти', 'type': 'bomb', 'toxicity': 15},
    {'name': 'Бомба удачи', 'type': 'bomb', 'toxicity': 8},
    {'name': 'Эликсир здоровья', 'type': 'potion', 'toxicity': 3},
    {'name': 'Кровь дракона', 'type': 'potion', 'toxicity': 20},
]

@app.route('/alchemy', methods=['GET'])
def alchemy():
    item_type = request.args.get('type')
    max_toxicity = request.args.get('toxicity', type=int)

    filtered_items = [
        item for item in alchemy_items
        if item['type'] == item_type and (max_toxicity is None or item['toxicity'] <= max_toxicity)
    ]

    return jsonify(filtered_items)

if __name__ == '__main__':
    app.run(debug=True)