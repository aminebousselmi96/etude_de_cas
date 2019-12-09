from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import Config

# Init app
app = Flask(__name__)
app.config.from_object(Config)

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
    name = db.Column(db.String(50), nullable=False)
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
@app.route('/user/<id_user>', methods=['GET'])
def get_user(id_user):
    user = User.query.get(id_user)
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
@app.route('/user/<id_user>', methods=['PUT'])
def update_user(id_user):
    user = User.query.get(id_user)

    last_name = request.json['last_name']
    first_name = request.json['first_name']
    birth_date = request.json['birth_date']

    user.last_name = last_name
    user.first_name = first_name
    user.birth_date = birth_date

    db.session.commit()

    return user_schema.jsonify(user)


# Add a realestate
@app.route('/realestate/<id_user>', methods=['POST'])
def add_realestate(id_user):
    user = User.query.get(id_user)
    
    new_real_estate = RealEstate(
        name = request.json['name'],
        description = request.json['description'],
        kind = request.json['kind'],
        town = request.json['town'].lower().strip(),
        nb_room = request.json['nb_room'],
        room_description = request.json['room_description'],
        owner=user
    )

    db.session.add(new_real_estate)
    db.session.commit()

    return real_estate_schema.jsonify(new_real_estate)

# Get all RealEstate of a specific city
@app.route('/realestate/<city_name>', methods=['GET'])
def get_realestates_city(city_name):
    all_real_estate = RealEstate.query.filter_by(town=city_name.lower().strip()).all()
    result = real_estates_schema.dump(all_real_estate)

    return jsonify(result)

# Update a realestate
@app.route('/realestate/<id_real_estate>/<id_user>', methods=['PUT'])
def update_realestate(id_real_estate, id_user):
    real_estate=RealEstate.query.get(id_real_estate)

    if real_estate.owner_id != int(id_user) : 
        return jsonify({"Acces denied":"You are not the owner"})
    else :
        user = User.query.get(id_user)
        
        real_estate.name = request.json['name']
        real_estate.description = request.json['description']
        real_estate.kind = request.json['kind']
        real_estate.town = request.json['town']
        real_estate.nb_room = request.json['nb_room']
        real_estate.room_description = request.json['room_description']

        db.session.commit()

        return real_estate_schema.jsonify(real_estate)



# Run Server
if __name__ == '__main__':
    app.run(debug=True)

