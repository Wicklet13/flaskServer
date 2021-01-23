from flask import Flask, render_template, request, redirect, json, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class arduinos(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    ad_id = db.Column(db.String(100), nullable = False, unique=True)
    usr_name = db.Column(db.String(15), nullable = False, unique=True)

    def __repr__(self):
        return "User #: " + str(self.id)


class arduinoData(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    ad_id = db.Column(db.String(100), db.ForeignKey('arduinos.ad_id'), nullable=False)
    steps = db.Column(db.Integer, nullable=False)

    arduinos = db.relationship('arduinos', backref="arduinoData")

    def __repr__(self):
        return self.ad_id + ' has ' + str(self.steps) + ' steps'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        data_usr = request.form['usr_name']
        data_id = request.form['ad_id']
        new_data = arduinos(ad_id=data_id, usr_name=data_usr)
        db.session.add(new_data)
        db.session.commit()
        return redirect('/data')
    else:
        all_data = arduinos.query.order_by(arduinos.usr_name).all()
        return render_template('data.html', data = all_data)

@app.route('/api/data', methods=['GET'])
def user_count():
    rows = db.session.query(arduinoData).order_by(arduinoData.steps).join(arduinos, arduinos.ad_id == arduinoData.ad_id).all()
    resp_arr = []
    for row in rows:
        data_dict = {
            'usr_name': row.arduinos.usr_name,
            'steps': row.steps
        }
        resp_arr.append(data_dict)

    return json.dumps(resp_arr)

@app.route('/api/user_steps/<string:usr>', methods=['GET'])
def usr_steps(usr):
    rows = db.session.query(arduinoData).join(arduinos, arduinos.ad_id == arduinoData.ad_id).filter_by(usr_name=usr)
    resp_arr = []
    for row in rows:
        data_dict = {
            'usr_name': row.arduinos.usr_name,
            'steps': row.steps
        }
        resp_arr.append(data_dict)

    return json.dumps(resp_arr)

@app.route('/api/arduinodata/<string:arduino>/<int:steps_counted>', methods=['POST'])
def post_data(arduino, steps_counted):
    new_data = arduinoData(ad_id=arduino, steps=steps_counted)
    db.session.add(new_data)
    db.session.commit()
    return redirect('/api/data')

@app.route('/data/delete/<int:id>')
def delete(id):
    data = arduinos.query.get_or_404(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/data')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)