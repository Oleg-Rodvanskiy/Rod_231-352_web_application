from flask import Flask, render_template

app = Flask(__name__)

@app.route('/witcher_profile')
def witcher_profile():
    witcher = {
        'name': 'Геральт из Ривии',
        'school': 'Школа Волка',
        'signs': ['Игни', 'Аард', 'Книн', 'Дельи'],
        'toxicity': 15,
        'health': 100,
        'experience': 2000
    }
    return render_template('witcher_profile.html', witcher=witcher)

if __name__ == '__main__':
    app.run(debug=True)