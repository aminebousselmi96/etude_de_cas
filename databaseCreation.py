from app import db, User, RealEstate

UserOne = User(last_name='Dupont', first_name='Jean', birth_date='12/03/1993')
UserTwo = User(last_name='Durand', first_name='Jeanne', birth_date='04/06/1991')
UserThree = User(last_name='Toutlemonde', first_name='Marie', birth_date='11/02/1997')

RealEstateOne = RealEstate(
    name='Flat 1',
    description='Student flat',
    kind='Flat',
    town='Valenciennes',
    nb_room='3',
    room_description='Living room, bathroom, bedroom',
    owner=UserOne,
)

RealEstateTwo = RealEstate(
    name='Flat 2',
    description='Family Flat',
    kind='Flat',
    town='Valenciennes',
    nb_room='6',
    room_description='Living room, bathroom, Parent\'s bedroom, Son\'s bedroom, Daughter \'s bedroom, kitchen',
    owner=UserTwo,
)

RealEstateThree = RealEstate(
    name='House 333',
    description='House in Valenciennes \' suburbs',
    kind='House',
    town='Famars',
    nb_room='7',
    room_description='Living room, bathroom, Parent\'s bedroom, Son\'s bedroom, Daughter \'s bedroom, kitchen, game room',
    owner=UserOne,
)


def feed_the_database():
    db.session.add_all([UserOne, UserTwo, UserThree, RealEstateOne, RealEstateTwo, RealEstateThree])
    db.session.commit()


# Create database
if __name__ == '__main__':
    db.create_all()

    # Check if the database is empty
    if (User.query.first() is None) & (RealEstate.query.first() is None):
        feed_the_database()
