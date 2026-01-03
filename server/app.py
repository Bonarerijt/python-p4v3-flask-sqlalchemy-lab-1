# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here


@app.route('/earthquakes/<int:id>', methods=['GET'])
def earthquakes(id):
    earthquake = Earthquake.query.get(id)
    if not earthquake:
        return make_response({'message': f'Earthquake {id} not found.'}, 404)
    return make_response(earthquake.to_dict(), 200)


@app.route('/earthquakes/magnitude/<float:magnitude>')
def magnitudes(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    data = [e.to_dict() for e in quakes]

    return make_response({'count': len(data), 'quakes': data}, 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
