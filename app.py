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
    real_estates = db.relationship('RealEstate', backref='owner', lazy='dynamic')

    def __init__(self,last_name,first_name,birth_date):
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date

    def __repr__(self):
        return '<User {} {}>'.format(self.last_name, self.first_name)
    

# Real Estate ClassModel
class RealEstate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(100))
    kind = db.Column(db.String(50))
    town = db.Column(db.String(50), nullable=False)
    nb_room = db.Column(db.Integer)
    room_description = db.Column(db.String(100))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return '<RealEstate {}>'.format(self.name)

 
# User Schema
class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

# RealEstate
class RealEstateSchema(ma.ModelSchema):
    class Meta:
        model = RealEstate


# Init schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)
real_estate_schema = RealEstateSchema()
real_estates_schema = RealEstateSchema(many=True)


@app.route('/', methods=['GET'])
def get():
    return jsonify({'Test': 'Hello World'})

# Get an User
@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

# Add an User
@app.route('/user', methods=['POST'])
def add_user():
    last_name = request.json['last_name']
    first_name = request.json['first_name']
    birth_date = request.json['birth_date']

    new_user = User(last_name, first_name, birth_date)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


# Update an User
@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)

    last_name = request.json['last_name']
    first_name = request.json['first_name']
    birth_date = request.json['birth_date']

    user.last_name = last_name
    user.first_name = first_name
    user.birth_date = birth_date

    db.session.commit()

    return user_schema.jsonify(user)

# Run Server
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
    
