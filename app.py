from datetime import datetime

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# DataBase
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)


# User ClassModel
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(20))
    birth_date = db.Column(db.String(20))

    def __init__(self, last_name, first_name, birth_date):
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date

 
# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','last_name', 'first_name', 'birth_date')


# Init schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/', methods=['GET'])
def get():
    return jsonify({'Test': 'Hello World'})

@app.route('/user', methods=['POST'])
def add_user():
    last_name = request.json['last_name']
    first_name = request.json['first_name']
    birth_date = request.json['birth_date']

    new_user = User(last_name, first_name, birth_date)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
