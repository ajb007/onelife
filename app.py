from flask import Flask, jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm.attributes import flag_modified
import os


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import *

@app.route('/create', methods=['POST'])
def create_player():
    # curl -i -H "Content-Type: application/json" -X POST -d '{"name":"Andy"}' http://localhost:5000/create
    if not request.json or not 'name' in request.json:
        abort(400)
    player = {
        'name': request.json['name'],
        'xpos': 0,
        'ypos': 0
    }
    try:
        result = Player(
            player=player
        )
        db.session.add(result)
        db.session.commit()
    except Exception as e:
        raise
    return jsonify({'player': player}), 201

@app.route('/player/<int:id>', methods=['GET'])
def get_player(id):
    player = Player.query.get(id).player
    print(player)
    #if player == None:
#        abort(404)
    return jsonify({'player': player}), 201

@app.route('/update/<int:id>', methods=['PUT'])
def update_player(id):

    # curl -i -H "Content-Type: application/json" -X PUT -d '{"name":"Drew"}' http://localhost:5000/update/10
    # Need to validate the request
    print("**************")
    print(request.get_json())
    updated_player = request.get_json()
    print("**************")
    try:
        player = Player.query.get(id)
        player.player = {
            'name': updated_player['name'],
            'xpos': updated_player['xpos'],
            'ypos': updated_player['ypos']
        }
        db.session.commit()
    except Exception as e:
        raise
    return jsonify({'player': player.player}), 201

@app.route('/')
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run()
