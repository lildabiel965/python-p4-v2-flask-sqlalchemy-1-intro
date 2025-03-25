from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate

from models import db, Pet

# create a Flask application instance
app = Flask(__name__)

# configure the database connection to the local file app.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# configure flag to disable modification tracking and use less memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create a Migrate object to manage schema modifications
migrate = Migrate(app, db)

# initialize the Flask application to use the database
db.init_app(app)

# Create a route to add a new pet
@app.route('/pets', methods=['POST'])
def add_pet():
    data = request.get_json()
    new_pet = Pet(name=data['name'], species=data['species'])
    db.session.add(new_pet)
    db.session.commit()
    return jsonify({'message': 'Pet added successfully!'}), 201

# Create a route to retrieve all pets
@app.route('/pets', methods=['GET'])
def get_pets():
    pets = Pet.query.all()
    return jsonify([{'id': pet.id, 'name': pet.name, 'species': pet.species} for pet in pets]), 200

# Create a route to retrieve a pet by ID
@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()

    if pet:
        body = pet.to_dict()
        status = 200
    else:
        body = {'message': f'Pet {id} not found.'}
        status = 404

    return make_response(body, status)

# Create a route to retrieve pets by species
@app.route('/species/<string:species>')
def pet_by_species(species):
    pets = []  # array to store a dictionary for each pet
    for pet in Pet.query.filter_by(species=species).all():
        pets.append(pet.to_dict())
    body = {'count': len(pets),
            'pets': pets
            }
    return make_response(body, 200)

# Create a route to update an existing pet
@app.route('/pets/<int:id>', methods=['PUT'])
def update_pet(id):
    data = request.get_json()
    pet = Pet.query.get_or_404(id)
    pet.name = data.get('name', pet.name)
    pet.species = data.get('species', pet.species)
    db.session.commit()
    return jsonify({'message': 'Pet updated successfully!'}), 200

# Create a route to delete a pet
@app.route('/pets/<int:id>', methods=['DELETE'])
def delete_pet(id):
    pet = Pet.query.get_or_404(id)
    db.session.delete(pet)
    db.session.commit()
    return jsonify({'message': 'Pet deleted successfully!'}), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
