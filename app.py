from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    dni = db.Column(db.String(20), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    dni = request.form['dni']

    existing_user = Usuario.query.filter_by(username=username).first()
    if existing_user:
        return render_template('index.html', error="Usuario ya registrado")

    new_user = Usuario(username=username, password=password, dni=dni)
    db.session.add(new_user)
    db.session.commit()

    return render_template('exito.html', username=username)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='miapp.local')
