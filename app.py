from flask import Flask, jsonify, request, send_from_directory, abort, make_response
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm.attributes import flag_modified
import os
from constants import MOVE_EVENT, MONSTER_EVENT
from jsonschema import validate
import json
from event import randomEvent
from fight import rollMonster

app = Flask(__name__, static_folder='data')
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import *
import playerTypes
from move import *

playerTypes.init()

@app.route('/login', methods=['POST'])
def login():
    if not request.json:
        abort(400)

    cred = request.json

    cursor = db.session.execute("SELECT id FROM account WHERE accountb #>> '{account,main,name}' = '%s'" % cred["name"])
    result=cursor.fetchone()
    if result:
        id = result
        cursor = db.session.execute("SELECT count(*) c FROM account WHERE accountb #>> '{account,main,password}' = '%s'" % cred["password"])
        result=cursor.fetchone()
        result = result[0]
        if result != 0:
            account = Account.query.get(id).account
            account["account"]["main"]["id"] = id[0]
            result = jsonify(account)
        else:
            result = {"result":"failure", "reason":"Incorrect account name or password"}
            abort(400, result)
    else:
        result = {"result":"failure", "reason":"Incorrect account name or password"}
        abort(400, result)

    return result, 201

@app.route('/create_account', methods=['POST'])
def create_account():
    # curl -i -H "Content-Type: application/json" -X POST -d '{"name":"Andy"}' http://localhost:5000/create
    if not request.json or not 'account' in request.json:
        abort(400)

    account = request.json
    my_schema = open("data/account.json").read()
    schema = json.loads(my_schema)
    valid = validate(account, schema)
    if validate(account, schema) == None:

        acc = account.get('account')
        main = acc.get('main')
        name = main.get('name')

        cursor = db.session.execute("SELECT count(*) c FROM account WHERE accountb #>> '{account,main,name}' = '%s'" % name)
        result=cursor.fetchone()
        result = result[0]
        if result == 0:

            try:
                account = Account(account=account)
                db.session.add(account)
                db.session.commit()
                result = {"result":"success", "reason":"", "id":account.id}
            except Exception as e:
                raise
        else:
            result = {"result":"failure", "reason":"Account exists already"}
            abort(400, result)

    else:
        result = {"result":"failure", "reason":"Invalid schema for Account"}
        abort(400, result)
    return jsonify(result), 201

#curl -i -X GET http://localhost:5000/create_player/Elf
# curl -i -H "Content-Type: application/json" -X POST -d '{"name":"Drew","xpos":0,"ypos":0,"action":0}' http://localhost:5000/create_player
@app.route('/create_player', methods=['POST'])
def create_player():
    if not request.json:
        abort(400)
    print(request.json)
    result = playerTypes.rollPlayerType(request.json)
    return jsonify(result), 201

@app.route('/save_player', methods=['POST'])
def save_player():
    if not request.json:
        abort(400)
    player_json = request.json
    cursor = db.session.execute("SELECT count(*) c FROM player WHERE playerb #>> '{name}' = '%s'" % player_json["player"]["main"]["name"])
    result=cursor.fetchone()
    result = result[0]
    if result == 0:
        try:
            player = Player(player=player_json, account_id=player_json["player"]["main"]["account_id"])
            db.session.add(player)
            db.session.commit()
            player_json["player"]["main"]["id"] = player.id
            player.player = player_json
            db.session.commit()
            result = {"result":"success", "reason":"","id":player.id}
        except Exception as e:
            raise
    else:
        result = {"result":"failure", "reason":"Character name already exists in realm"}
        abort(400, result)

    return jsonify(result), 201

@app.errorhandler(400)
def not_found(error):
    return jsonify(error.description), 400

@app.route('/players/<int:account_id>', methods=['GET'])
def get_players(account_id):
    players = Player.query.with_entities(Player.player).filter(Player.account_id == account_id).all()
    #if player == None:
#        abort(404)
    return jsonify({'players': players}), 201

@app.route('/player/<int:id>', methods=['GET'])
def get_player(id):
    player = Player.query.get(id).player
    #if player == None:
#        abort(404)
    return jsonify({'player': player}), 201

# Player Action: An action has occurred in the client. Process it on the server
@app.route('/action/<int:id>', methods=['PUT'])
def update_player(id):

    # curl -i -H "Content-Type: application/json" -X PUT -d '{"name":"Drew","xpos":0,"ypos":0,"action":0}' http://localhost:5000/action/2
    # Need to validate the request
    updated_player = request.get_json()
    # Process action
    action = updated_player["action"]
    if action["type"] == MOVE_EVENT:
        doMoveAction(updated_player)
    try:
        player = Player.query.get(id)
        player.player = updated_player
        db.session.commit()
    except Exception as e:
        raise
    # Generate a reaction
    updated_player["reaction"] = randomEvent(updated_player)

    if updated_player["reaction"]["type"] == MONSTER_EVENT:
        rollMonster(updated_player)

    return jsonify(updated_player), 201

@app.route('/data/<path:filename>', methods=['GET'])
def get_data():
    return send_from_directory(app.static_folder, filename)

# Player Event: Client is checking for queued events. Return event for the
# client to respond
@app.route('/event/<int:id>', methods=['GET'])
def player_event(id):
    # curl -i GET http://localhost:5000/event/2
    player = Player.query.get(id).player
    player = event.checkForEvent(player)
    return jsonify({'player': player}), 201


@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run()
