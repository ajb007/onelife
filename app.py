from flask import Flask, jsonify, request, send_from_directory, abort, make_response
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm.attributes import flag_modified
import os
from constants import (
    MOVE_EVENT, MONSTER_EVENT, ATTACK_EVENT, GURU_EVENT, REST_EVENT,
    TREASURE_EVENT, TELEPORT_EVENT,
    MESSAGE_RESPONSE, MONSTER_CALL, MONSTER_SPECIFY,
    MESSAGE_YES, MESSAGE_NO, MESSAGE_NOALL
    )
from jsonschema import validate
import json
from event import randomEvent, monsterInBattleEvent, nextEvent, stackEvent, cancelTreasureEvents
from fight import rollMonster, doPlayerHits
from playerTypes import rollPlayerType
from misc import doGuru
from stats import doSin

app = Flask(__name__, static_folder='data')
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import *
from stats import *
from move import *

import treasure
from treasure import doTreasure, _answerGems

initPlayerTypes()

@app.route('/login', methods=['POST'])
def login():
    if not request.json:
        abort(400)

    cred = request.json

    cursor = db.session.execute("SELECT id FROM accounts WHERE accountb #>> '{account,main,name}' = '%s'" % cred["name"])
    result=cursor.fetchone()
    if result:
        id = result
        cursor = db.session.execute("SELECT count(*) c FROM accounts WHERE accountb #>> '{account,main,password}' = '%s'" % cred["password"])
        result=cursor.fetchone()
        result = result[0]
        if result != 0:
            account = Accounts.query.get(id).account
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

        cursor = db.session.execute("SELECT count(*) c FROM accounts WHERE accountb #>> '{account,main,name}' = '%s'" % name)
        result=cursor.fetchone()
        result = result[0]
        if result == 0:

            try:
                account = Accounts(account=account)
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
    result = rollPlayerType(request.json)
    return jsonify(result), 201

@app.route('/save_player', methods=['POST'])
def save_player():
    if not request.json:
        abort(400)
    player_json = request.json
    cursor = db.session.execute("SELECT count(*) c FROM players WHERE playerb #>> '{name}' = '%s'" % player_json["player"]["main"]["name"])
    result=cursor.fetchone()
    result = result[0]
    if result == 0:
        try:
            player = Players(player=player_json, account_id=player_json["player"]["main"]["account_id"])
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
    players = Players.query.with_entities(Players.player).filter(Players.account_id == account_id).all()
    #if player == None:
#        abort(404)
    return jsonify({'players': players}), 201

@app.route('/player/<int:id>', methods=['GET'])
def get_player(id):
    player = Players.query.get(id).player
    #if player == None:
#        abort(404)
    return jsonify({'player': player}), 201

# Player Action: An action has occurred in the client. Process it on the server
@app.route('/action/<int:id>', methods=['PUT'])
def update_player(id):

    # curl -i -H "Content-Type: application/json" -X PUT -d '{"name":"Drew","xpos":0,"ypos":0,"action":0}' http://localhost:5000/action/2
    # Need to validate the request
    payload = request.get_json()
    # Process action if there is one
    if "action" in payload.keys():
        action = payload["action"]
        if action["type"] == MOVE_EVENT:
            doMoveAction(payload)
        elif action["type"] == ATTACK_EVENT:
            doPlayerHits(payload)
        elif action["type"] == REST_EVENT:
            doRest(payload["player"])
        elif action["type"] == MESSAGE_RESPONSE:
            if action["arg1"] == MESSAGE_YES:
                msg = dict(action["message"])
                methodToCall = getattr(treasure, msg["callback"])
                methodToCall(payload)
            if action["arg1"] == MESSAGE_NO and action["message"] != "":
                # may want to do something on a "No" response. E.g. refuse ring to Nazgul
                msg = dict(action["message"])
                methodToCall = getattr(treasure, msg["callback"])
                methodToCall(payload)
            if action["arg1"] == MESSAGE_NOALL:
                # Only applicable to cancelling all treasure_type
                cancelTreasureEvents(payload)
        elif action["type"] == MONSTER_EVENT and action["arg1"] == MONSTER_CALL:
            # Monster hunted. Stack the event
            doSin(payload["player"], .001)
            event = newEvent(action["type"], action["arg1"], action["arg2"], action["arg3"], "")
            stackEvent(payload, event)
        elif action["type"] == MONSTER_EVENT and action["arg1"] == MONSTER_SPECIFY:
            print("Scroll Picked")
            # stack the event and process it straight away
            event = newEvent(action["type"], action["arg1"], action["arg2"], action["arg3"], "")
            stackEvent(payload, event)
            payload["reaction"] = nextEvent(payload)
            rollMonster(payload)
        elif action["type"] == TELEPORT_EVENT:
            print(payload["action"])
            doTeleport(payload)
        # remove the action now that we are done with it
        del payload["action"]

    # Save the payload
    try:
        player = Players.query.get(id)
        player.player = payload
        db.session.commit()
    except Exception as e:
        raise

    # if the opponent no longer exists then we are done with the battle
    inBattle = False
    if "battle" in payload["player"].keys():
        battle = payload["player"]["battle"]
        if "opponent" in battle.keys():
            if battle["opponent"]["energy"] > 0:
                # still in battle. Regenerate the monster event
                inBattle = True
                payload["reaction"] = monsterInBattleEvent(payload)
                return jsonify(payload), 201

    # Check if there is a stacked event
    if "events" in payload.keys():
        if len(payload["events"]) > 0:
            payload["reaction"] = nextEvent(payload)
    # Else generate a reaction
    elif not inBattle:
        payload["reaction"] = randomEvent(payload)

    # Process the reaction now if we can

    if payload["reaction"]["type"] == MONSTER_EVENT and payload["reaction"]["arg1"] != MONSTER_SPECIFY:
        rollMonster(payload)
    elif payload["reaction"]["type"] == GURU_EVENT:
        doGuru(payload)
    elif payload["reaction"]["type"] == TREASURE_EVENT and payload["reaction"]["message"] == "":
        doTreasure(payload)

    return jsonify(payload), 201

@app.route('/data/<path:filename>', methods=['GET'])
def get_data():
    return send_from_directory(app.static_folder, filename)

# Not in use
@app.route('/answer/<int:id>', methods=['PUT'])
def player_event(id):
    # curl -i GET http://localhost:5000/event/2
    return jsonify(payload), 201


@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run()
