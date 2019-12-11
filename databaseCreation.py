from app import db, User, RealEstate

# Creation of three fictional users
UserOne = User(last_name='Dupont', first_name='Jean', birth_date='12/03/1993')
UserTwo = User(last_name='Durand', first_name='Jeanne', birth_date='04/06/1991')
UserThree = User(last_name='Toutlemonde', first_name='Marie', birth_date='11/02/1997')

# Creation of three fictional real estates
RealEstateOne = RealEstate(
    name='flat 1',
    description='student flat',
    kind='flat',
    town='valenciennes',
    nb_room='3',
    room_description='living room, bathroom, bedroom',
    owner=UserOne,
)

RealEstateTwo = RealEstate(
    name='flat 2',
    description='family flat',
    kind='flat',
    town='valenciennes',
    nb_room='6',
    room_description='living room, bathroom, parent\'s bedroom, son\'s bedroom, daughter \'s bedroom, kitchen',
    owner=UserTwo,
)

RealEstateThree = RealEstate(
    name='house 3',
    description='house in valenciennes \' suburbs',
    kind='house',
    town='famars',
    nb_room='7',
    room_description='living room, bathroom, parent\'s bedroom, son\'s bedroom, daughter \'s bedroom, kitchen, game room',
    owner=UserOne,
)


# Function to fill the database
def feed_the_database():
    db.session.add_all([UserOne, UserTwo, UserThree, RealEstateOne, RealEstateTwo, RealEstateThree])
    db.session.commit()


# Creation of the database
if __name__ == '__main__':
    # create_all() create the database only if it does not already exist
    db.create_all()
    # Check if the database is empty, if not we do not fill it with our data
    if (User.query.first() is None) & (RealEstate.query.first() is None):
        feed_the_database()
