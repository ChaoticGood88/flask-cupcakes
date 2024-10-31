"""Flask app for Cupcakes"""
from flask import Flask, jsonify, request, abort, render_template
from models import db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/api/cupcakes', methods=['GET'])
def get_all_cupcakes():
    """Get data about all cupcakes."""
    cupcakes = Cupcake.query.all()
    serialized = [{
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    } for cupcake in cupcakes]
    return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['GET'])
def get_cupcake(cupcake_id):
    """Get data about a single cupcake."""
    cupcake = Cupcake.query.get(cupcake_id)
    if not cupcake:
        abort(404, description="Cupcake not found")
    serialized = {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }
    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create a new cupcake."""
    data = request.json

    # Provide default image URL if not supplied
    image = data.get('image', 'https://tinyurl.com/demo-cupcake')
    cupcake = Cupcake(
        flavor=data['flavor'],
        size=data['size'],
        rating=data['rating'],
        image=image
    )

    db.session.add(cupcake)
    db.session.commit()

    serialized = {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }
    return jsonify(cupcake=serialized), 201

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """Update a cupcake with the given ID."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    data = request.json
    cupcake.flavor = data['flavor']
    cupcake.size = data['size']
    cupcake.rating = data['rating']
    cupcake.image = data['image']

    db.session.commit()

    serialized = {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }
    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """Delete a cupcake with the given ID."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")

@app.route('/')
def homepage():
    """Show homepage with an empty cupcake list and a form to add new cupcakes."""
    return render_template('index.html')




