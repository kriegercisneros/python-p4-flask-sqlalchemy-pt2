#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet, Owner

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#this avoids building up too much unhelpful data in memory when our application is running 

#configures the application and models for Flask-Migrate
migrate = Migrate(app, db)

# connects our db to our application before it runs
db.init_app(app)

#determines which resoures are available at which URLs and saves them to 
#the application's URL map
@app.route('/')
def index():
    #we return responses to the client after a request.  this one has a status 
    #code of 200, which means the resource exists an is accessible at the URL
    response = make_response(
        '<h1>Welcome to the pet/owner directory!</h1>', 200
    )
    return response

@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id ==id).first()

    if not pet:
        response_body = '<h1>404 pet not found</h1>'
        response = make_response(response_body, 404)
        return response

    response_body = f'''
    <h1>Information for {pet.name}</h1>
    <h2>Pet Species is {pet.species}</h2>
    <h2>Pet owner is {pet.owner.name}</h2>
    '''

    response = make_response(response_body, 200)

    return response

@app.route('/owner/<int:id>')
def owner_by_id(id):
    owner = Owner.query.filter(Owner.id ==id).first()

    if not owner:
        response_body = '<h1>404 owner not found</h1>'
        response = make_response(response_body, 404)
        return response
    
    response_body = f'<h1>Information for {owner.name}</h1>'

    pets = [pet for pet in owner.pets]

    if not pets:
        response_body += f'<h2>Has no pets at this time.</h2>'

    else:
        for pet in pets:
            response_body += f'<h2>Has pet {pet.species} named {pet.name}.</h2>'

    response = make_response(response_body, 200)

    return response
    pass

if __name__ == '__main__':
    app.run(port=5555, debug=True)
