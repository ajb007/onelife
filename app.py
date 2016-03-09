from flask import Flask, jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import *

@app.route('/create', methods=['POST'])
def create_player():
    print('Here')
    if not request.json or not 'player' in request.json:
        abort(400)
    player = {
        'name': request.json['player'],
        'xpos': 0,
        'ypos': 0,
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
def get_task(id):
    player = Player.query.get(id).player
    print(player)
    #if player == None:
#        abort(404)
    return jsonify({'player': player}), 201

@app.route('/')
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run()
