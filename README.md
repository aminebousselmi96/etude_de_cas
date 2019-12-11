# Arcane Project

Arcane Project is REST API in python using : 

  - Flask
  - SQLAlchemy
  - Marshmallow

## Getting started

### Prerequesites
You need to have : 
* 3.7 python installed : https://www.python.org/downloads/release/python-370/

* Pipenv installed : 
```sh
# Install pipenv
$ pip3 install pipenv
```
See as well the [Pipenv documentation] 

### Installation
Once you have cloned the repository and are in it, you need to activate venv :
```sh
# Activate venv
$ pipenv shell
```
Then you need to install dependencies :
```sh
# Install dependencies automatically
$ pipenv install
```

## Run the server
### First use
You need to create your local SQlite Database :
```sh
# Create DB and fill it with fictional data
$ python databaseCreation.py
```

### Run the server
To run the server :
```sh
# Run server (http://localhost:5000)
$ python app.py
```

### Endpoints
Here is a list of all the api endpoints : (.../ means where you run your server : ex =  http://localhost:5000)

| Number| HTTP Method | Action | Route
| ------| ------ | ------ | ------ |
| 1 | GET  | Get an user | .../user/<int:id_user> |
| 2 | POST  | Add an User | .../user |
| 3 | PUT  | Update an user | .../user/<int:id_user> |
| 4 | POST  | Add a realestate | /realestate/<int:id_user> |
| 5 | GET  | Get all real estates of a specific city | .../realestate/<city_name>|
| 6 | PUT  | Update a real estate | .../realestate/<int:id_real_estate>/<int:id_user> |

Be careful : only requests with a application/json Content-Type are accepted

* For request 2 and 3, the body request must be similar to this : 
```sh
{
	"last_name" : "Desmarchelier",
	"first_name" : "Pierre",
	"birth_date" : "21/02/1996"
}
```
* For request 4 and 6, the body request must be similar to this : 
```sh
{
	"name":"student flat in lille",
    "description":"student flat",
    "kind":"flat",
    "town":"lille",
    "nb_room":"1",
    "room_description": "Living room"
}
```

To test the endpoints, I strongly recommend to use [Postman]
You can find here a collection of the different requests : [![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/35b0ba5a6e7a72c6a72f)



[//]: #
   [postman]: <https://www.getpostman.com>
   [pipenv documentation]: <https://pypi.org/project/pipenv/>
