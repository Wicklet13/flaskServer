from flask import Flask, render_template, request, redirect
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class arduinos(db.Model):
    __tablename__ = 'arduinos'
    id = db.Column(db.Integer, primary_key = True)
    ad_id = db.Column(db.String(100), nullable = False)
    usr_id = db.Column(db.String(15), nullable = False)
    arduinoData = db.relationship('arduinoData', backref='arduinos', lazy=True)

    def __repr__(self):
        return 'User #' + str(self.id)

class arduinoData(db.Model):
    __tablename__ = 'arduinoData'
    id = db.Column(db.Integer, primary_key = True)
    ad_id = db.Column(db.String(100), db.ForeignKey('arduinos.ad_id'), nullable=False)
    steps = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return self.ad_id + ' has ' + str(self.steps) + ' steps'

arduino_data_put_args = reqparse.RequestParser()
arduino_data_put_args.add_argument("ad_id", type=str, help="arduino id is required", required=True)
arduino_data_put_args.add_argument("steps", type=int, help="steps are required", required=True)

resource_fields = {
    ''
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        data_usr = request.form['usr_id']
        data_id = request.form['ad_id']
        new_data = arduinos(ad_id=data_id, usr_id=data_usr)
        db.session.add(new_data)
        db.session.commit()
        return redirect('/data')
    else:
        all_data = arduinos.query.order_by(arduinos.usr_id).all()
        return render_template('data.html', data = all_data)

@app.route('/data/delete/<int:id>')
def delete(id):
    post = arduinos.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/data')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)