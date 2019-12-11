from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import Config

# Init app
app = Flask(__name__)
app.config.from_object(Config)

# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)


# User ClassModel
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(50))
    first_name = db.Column(db.String(20))
    birth_date = db.Column(db.String(20))
    real_estates = db.relationship('RealEstate', backref='owner', lazy='dynamic')

    def __init__(self, last_name, first_name, birth_date):
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date

    def __repr__(self):
        return '<User {} {}>'.format(self.last_name, self.first_name)


# Real Estate ClassModel
class RealEstate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(100))
    kind = db.Column(db.String(50))
    town = db.Column(db.String(50))
    nb_room = db.Column(db.Integer)
    room_description = db.Column(db.String(100))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<RealEstate {}>'.format(self.name)


# User Schema
class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


# RealEstate schema
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
@app.route('/user/<int:id_user>', methods=['GET'])
def get_user(id_user):
    # Database call
    user = User.query.get(id_user)

    # If no users found, an error is sent
    if user is None:
        return jsonify({'No matches found': 'No user with the id : ' + str(id_user)}), 400

    # Else all the user information is sent
    return user_schema.jsonify(user)


# Add an User
@app.route('/user', methods=['POST'])
def add_user():
    # Check if the request is json
    if not request.is_json:
        return jsonify({'Invalid request': 'Mimetype is not application/json or application/*+json'}), 400
    else:
        # Check if the request is well formed
        if all(arg in request.json.keys() for arg in ["last_name", "first_name", "birth_date"]):
            last_name = request.json['last_name']
            first_name = request.json['first_name']
            birth_date = request.json['birth_date']

            # Creation of the new user
            new_user = User(last_name, first_name, birth_date)
            db.session.add(new_user)
            db.session.commit()

            return user_schema.jsonify(new_user)
        else:
            return jsonify({'Error': 'Missing argument in the request'}), 400


# Update an User
@app.route('/user/<int:id_user>', methods=['PUT'])
def update_user(id_user):
    # Check if the request is json
    if not request.is_json:
        return jsonify({'Invalid request': 'Mimetype is not application/json or application/*+json'}), 400
    else:
        user = User.query.get(id_user)
        # If no users found, an error is sent
        if user is None:
            return jsonify({'No matches found': 'No user with the id : ' + str(id_user)}), 400
        # Check if the request is well formed
        elif not all(arg in request.json.keys() for arg in ["last_name", "first_name", "birth_date"]):
            return jsonify({'Error': 'Missing argument in the request'}), 400
        else:
            last_name = request.json['last_name']
            first_name = request.json['first_name']
            birth_date = request.json['birth_date']

            # Update of the user
            user.last_name = last_name
            user.first_name = first_name
            user.birth_date = birth_date

            db.session.commit()

            return user_schema.jsonify(user)


# Add a realestate
@app.route('/realestate/<int:id_user>', methods=['POST'])
def add_realestate(id_user):
    # Check if the request is json
    if not request.is_json:
        return jsonify({'Invalid request': 'Mimetype is not application/json or application/*+json'}), 400
    else:
        user = User.query.get(id_user)
        # If no users found, an error is sent
        if user is None:
            return jsonify({'No matches found': 'No user with the id : ' + str(id_user)}), 400
        # Check if the request is well formed
        elif not all(arg in request.json.keys() for arg in
                     ["name", "description", "kind", "town", "nb_room", "room_description"]):
            return jsonify({'Error': 'Missing argument in the request'}), 400
        else:
            # Creation of the new real estate
            new_real_estate = RealEstate(
                name=request.json['name'],
                description=request.json['description'],
                kind=request.json['kind'],
                town=request.json['town'].lower().strip(),
                nb_room=request.json['nb_room'],
                room_description=request.json['room_description'],
                owner=user
            )

            db.session.add(new_real_estate)
            db.session.commit()

            return real_estate_schema.jsonify(new_real_estate)


# Get all RealEstate of a specific city
@app.route('/realestate/<city_name>', methods=['GET'])
def get_realestates_city(city_name):
    # Database call for selecting all real estate of a specific town
    all_real_estate = RealEstate.query.filter_by(town=city_name.lower().strip()).all()
    # If no real estates found, an error is sent
    if not all_real_estate:
        return jsonify({'No matches found': 'No real Estate in : ' + str(city_name)}), 400
    else:
        result = real_estates_schema.dump(all_real_estate)
        return jsonify(result)


# Update a realestate
@app.route('/realestate/<int:id_real_estate>/<int:id_user>', methods=['PUT'])
def update_realestate(id_real_estate, id_user):
    # Check if the request is json
    if not request.is_json:
        return jsonify({'Invalid request': 'Mimetype is not application/json or application/*+json'}), 400
    else:
        real_estate = RealEstate.query.get(id_real_estate)
        # If no real estates found, an error is sent
        if real_estate is None:
            return jsonify({'No matches found': 'No real Estate with the id : ' + str(id_real_estate)}), 400
        # If no users found, an error is sent
        user = User.query.get(id_user)
        if user is None:
            return jsonify({'No matches found': 'No user with the id : ' + str(id_user)}), 400
        # Check if the user owns the real estate
        elif real_estate.owner_id != int(id_user):
            return jsonify({"Access denied": "You are not the owner"}), 400
        else:
            # Check if the request is well formed
            if not all(arg in request.json.keys() for arg in
                       ["name", "description", "kind", "town", "nb_room", "room_description"]):
                return jsonify({'Error': 'Missing argument in the request'}), 400
            else:
                # Update of the real estate
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
