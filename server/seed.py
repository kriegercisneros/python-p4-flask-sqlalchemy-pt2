'''remember this is a shebang operator which specifies the interpreter to be 
used to run the script'''
#!/usr/bin/env python3

from random import choice as rc
'''imports the choice function from the random moduel as alias rc'''

from faker import Faker
'''imports the faker class from the faker moduel'''

from app import app

'''imports the app instance from a moduel named app'''
from models import db, Owner, Pet

fake = Faker()
'''creates an instance of the faker class to generate fake data'''
#create an application context before we begin.  it will not necessarily be used
#but will ensure that apps fail quickly if they are not configured with this context
with app.app_context():
    '''opens a flask application context'''

    #deletion of all records handles as below vs vanilla: session.query(Model).delete()
    Pet.query.delete()
    Owner.query.delete()

    owners = []
    for n in range(50):
        owner = Owner(name=fake.name())
        owners.append(owner)

    db.session.add_all(owners)

    pets = []
    species = ['Dog', 'Cat', 'Chicken', 'Hamster', 'Turtle']
    for n in range(100):
        pet = Pet(name=fake.first_name(), species=rc(species), owner=rc(owners))
        '''creates an instace of the Pet class with a randomly generated first name
        using fake.first_name() method, a randomly select owner using the 
        rc(owners) method and a randomly selected species using the rc(species) method'''
        pets.append(pet)

    db.session.add_all(pets)
    db.session.commit()
