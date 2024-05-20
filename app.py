from flask import Flask, render_template, redirect, url_for, request, flash, session, abort, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import boto3
import os
from dotenv import load_dotenv

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

load_dotenv()
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
S3_IMAGE_KEY = os.getenv('S3_IMAGE_KEY')

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
    s3 = boto3.client('s3')

    try:
        image_object = s3.get_object(Bucket=S3_BUCKET_NAME, Key=S3_IMAGE_KEY)
        image_data = Response(
            image_object['Body'].read(),
            mimetype='image/jpeg',
            headers={
                "Content-Disposition": "inline; filename={}".format(image_object)
            }
        )

        print(f"image_data: {image_data}")
    except Exception as e:
        print(f"Error fetching image from S3: {e}")
        image_data = None

    return render_template("user_details.html", user=user, image_data=image_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)

