from flask import Flask, render_template, redirect, url_for, request, flash, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(250), nullable=False)


@app.route('/', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        user = User(name=name, email=email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user_details', user_id=user.id))
    return render_template('create_user.html')


@app.route("/user_details/<user_id>")
def user_details(user_id):
    user = User.query.get(user_id)
    bucket_name = 'kely-bucket-160524'
    image_key = 'river.jpeg'
    image_url = f'https://{bucket_name}.s3.amazonaws.com/{image_key}'
    return render_template("user_details.html", user=user, image_url=image_url)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)

