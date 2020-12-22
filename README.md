# Arar inventory App 


Ararapp it's an app that tracks the inventory of differrent devices that are rented in different companies.


#### Where can I access the app?
Arapp has been deployed to Heroku and is currently working at this link:</br> 
<strong>[https://arar-dev.herokuapp.com/](https://arar-dev.herokuapp.com/)</strong>


## Dependencies
To access the app locally, you need a database, a virtual environment, dependencies installed, and environment variables set up. You also need an account with Auth0, an authentication service.

1. This app runs on a PostgreSQL database. You can download PostgreSQL at [postgresql.org](https://www.postgresql.org/download/).
2. Then head to [Auth0.com](https://auth0.com/) to create an account.
3. Next, activate a virtual environment:
```
$ cd project_directory_path/
$ virtualenv env
$ source env/bin/activate
```
3. Set up environment variables:
```
$ source setup.sh
```
4. Install dependencies
```
pip install -r requirements.txt
```

## Setup
1. Create a PostgreSQL database locally and connect to it from setup.sh:
```
export DATABASE_URL='postgresql://{{USER}}@localhost:{{PORT}}/{{DATABASE_NAME}}'
```
2. Run database migrations
```
flask db init 
flask db migrate
flask db upgrade
```
3. In Auth0, configure a single page web application and its API, relying on the environment variables in setup.sh.
4. Start the development server:  
```
$ export FLASK_APP=app.py 
$ export FLASK_ENV=development # enables debug mode  
$ flask run --reload
```

## Usage

### Arar app roles

<strong>Manager</strong>: Full access, with the ability to view, list, update, and delete items, item_types, owners and inventory locations
```
Manager login credentials
User: mile@morales.de
Password: Password123
```

<strong>Client</strong>: They only have the option to list items, item_types, owners and inventory locations, with out the ability to manage them
```
Executive producer login credentials
User: spider@ham.de
Password: Password123 
```

### API endpoints
To access this app's API, a user needs to be authenticated. Logging in with approved credentials generates a JWT (JSON Web Token) that grants the user access based on their role's permissions.


#### GET /items/types
- Returns a list of all item
- Roles authorized: all users
- Sample: ```curl http://127.0.0.1:5000/items/types```

#### GET /owners
- Returns a list of all owners
- Roles authorized: all users
- Sample: ```curl http://127.0.0.1:5000/owners```

#### GET /inventory-locations
- Returns a list of all inventory locations
- Roles authorized: all users
- Sample: ```curl http://127.0.0.1:5000/inventory-locations```

#### GET /items
- Returns a list of all items
- Roles authorized: all users
- Sample: ```curl http://127.0.0.1:5000/items```


#### POST /items/types
- Adds a new item type to the database
- Roles authorized: manager
- Sample: ```curl http://127.0.0.1:5000/items/types -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {AUTH_TOKEN}" -d '{ "name": "Printers" }'```

#### POST /owners
- Adds a new owner to the database
- Roles authorized: manager
- Sample: ```curl http://127.0.0.1:5000/owners -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {AUTH_TOKEN}" -d '{ "new_email": "ezra@klein.de", "name": "Ezra Klein" }'```

#### POST /inventory-locations
- Adds a new inventory location to the database
- Roles authorized: manager
- Sample: ```curl http://127.0.0.1:5000/inventory-locations -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {AUTH_TOKEN}" -d '{ "new_name": "Lager", "new_address": "Oudenarder Strasse 30", "description": "Haus", "image_url": "https://upload.wikimedia.org/wikipedia/commons/7/72/Haus_Bisping.jpg" }'```

#### PATCH /items/types/:id
- Changes item type provided with the id
- Roles authorized: manager
- Sample: ```curl http://localhost:5000/items/types/1 -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer {AUTH_TOKEN}" -d '{ "name": "Laptop"}'```

#### PATCH /owners/:id
- Changes owner provided with the id
- Roles authorized: manager
- Sample: ```curl http://localhost:5000/owners/1 -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer {AUTH_TOKEN}" -d '{ "name": "Rafael Nadal"}'```

#### PATCH /inventory-location/:id
- Changes inventory-location provided with the id
- Roles authorized: manager
- Sample: ```curl http://localhost:5000/inventory-location/1 -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer {AUTH_TOKEN}" -d '{ "name": "Hinter Haus"}'```

#### DELETE /items/types/:id
- Deletes an item type from the database with the id 
- Roles authorized: manager
- Sample: ```curl http://localhost:5000/items/types/1 -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {AUTH_TOKEN}"```

#### DELETE /owners/:id
- Deletes an owner from the database with the id 
- Roles authorized: manager
- Sample: ```curl http://localhost:5000/owners/1 -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {AUTH_TOKEN}"```

#### DELETE /inventory-location/:id
- Deletes an inventory location from the database with the id 
- Roles authorized: manager
- Sample: ```curl http://localhost:5000/inventry-location/1 -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {AUTH_TOKEN}"```


### Error handling
The error codes currently returned are:
- 400: Bad request  
- 401: Unauthorized
- 403: Forbidden
- 404: Not found
- 405: Method not allowed
- 422: Unprocessable
- 500: Internal server error
- AuthError: Auth0 error status code and description
