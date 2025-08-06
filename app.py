from flask import jsonify
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from forms import calculate_bmr

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calorie_counter.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret123'

db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        age = int(request.form['age'])
        gender = request.form['gender']
        activity = request.form['activity']
        goal = request.form['goal']

        bmr = calculate_bmr(gender, weight, height, age)
        tdee = bmr * float(activity)

        if goal == 'lose':
            recommended = tdee - 500
        else:
            recommended = tdee

        user = User(
            name=name,
            weight=weight,
            height=height,
            age=age,
            gender=gender,
            activity=float(activity),
            bmr=bmr,
            tdee=tdee,
            recommended_calories=recommended
        )
        db.session.add(user)
        db.session.commit()

        return render_template('result.html', user=user)

    return render_template('register.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    data = request.get_json()
    name = data['name']
    weight = float(data['weight'])
    height = float(data['height'])
    age = int(data['age'])
    gender = data['gender']
    activity = float(data['activity'])
    goal = data['goal']

    bmr = calculate_bmr(gender, weight, height, age)
    tdee = bmr * activity
    recommended = tdee - 500 if goal == 'lose' else tdee

    return jsonify({
        'bmr': bmr,
        'tdee': tdee,
        'recommended_calories': recommended
    })

