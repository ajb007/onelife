from math import floor, ceil, cos, sin, sqrt, fabs
from flask import jsonify
from macros import sgn
from random import random
from event import newEvent
import numpy
from constants import (
    PL_REALM, PL_THRONE, PL_EDGE, PL_VALHALLA, PL_PURGATORY, D_CIRCLE,
    A_NEAR, A_FAR, A_BANISH, A_OUST, A_TRANSPORT, A_FORCED, A_SPECIFIC, A_TELEPORT,
    D_EDGE, D_BEYOND, DEATH_EVENT, K_FELL_OFF,
    B_NORTH, B_NORTH_EAST, B_EAST, B_SOUTH_EAST, B_SOUTH, B_SOUTH_WEST, B_WEST, B_NORTH_WEST
)
def setLocation(location):

    quadrant = 0       # quandrant of grid
    error_msg = ""
    nametable = numpy.array (  # names of places
        [("Anorien","Ithilien","Rohan","Lorien"),
        ("Gondor","Mordor","Dunland","Rovanion"),
        ("South Gondor","Khand","Eriador","The Iron Hills"),
        ("Far Harad","Near Harad","The Northern Waste","Rhun")]
        )

    if location["location"] == PL_REALM:
        if location["beyond"]:
            location["area"] = "The Point of No Return"
        elif location["circle"] >= 400.0:
            location["area"] = "The Ashen Mountains"
        elif location["circle"] >= 100:
            location["area"] = "Kennaquahir"
        elif location["circle"]>= 36:
            location["area"] = "Morannon"
        elif location["circle"] == 27 or location["circle"] == 28:
            location["area"] = "The Cracks of Doom"
        elif location["circle"] > 24 and location["circle"] < 31:
            location["area"] = "The Plateau of Gorgoroth"
        elif location["circle"] >= 20:
            location["area"] = "The Dead Marshes"
        elif location["circle"] >= 10:
            location["area"] = "The Outer Waste"
        elif location["circle"] >= 5:
            location["area"] = "The Moors Adventurous"
        else:
            # this expression is split to prevent compiler loop with some compilers
            quadrant = 1 if location["x"] > 0.0 else 0
            quadrant += 2 if location["y"] >= 0.0 else 0
            circle = int(location["circle"])
            location["area"] = nametable[circle - 1,quadrant]

    elif location["location"] == PL_THRONE:
        location["area"] = "The Lord's Chamber"
    elif location["location"] == PL_EDGE:
        location["area"] = "Edge Of The Realm"
    elif location["location"] == PL_VALHALLA:
        location["area"] = "Valhalla"
    elif location["location"] == PL_PURGATORY:
        location["area"] = "Purgatory"
	# no other places to be
    else:
        location["area"] = "State Of Insanity"
        error_msg = "Bad area in nameLocation"
        #"[%s] Bad c->location.area of %hd in Do_name_location.\n",
		#c->connection_id, c->location.area);

def setCircle(location):
    distance = getDistance(location["x"], 0.0, location["y"], 0.0)
    location["circle"] = floor(distance / D_CIRCLE + 1)

def getDistance(x1, x2, y1, y2):
    deltax = x1 - x2
    deltay = y1 - y2
    return sqrt(deltax * deltax + deltay * deltay)

def doMoveClose(x, y, maxDistance):

    angle = 0.0
    distance = 0.0
    angle = random() * 2 * 3.14159
    distance = random() * maxDistance
    if (distance < 1.0):
	    distance = 1.0

    c = floor(cos(angle) * distance + .5)
    s = floor(sin(angle) * distance + .5)

	# add half a point because floor(-3.25) = -4 */
    x += floor(cos(angle) * distance + .5)
    y += floor(sin(angle) * distance + .5)

    return x, y

def doMoveAction(payload):
    doMove(payload)
    setLocation(payload["player"]["location"])
    setCircle(payload["player"]["location"])

def doMove(payload):

    x = 0
    y = 0

    action = payload["action"]
    player = payload["player"]
    location = player["location"]
    status = player["status"]
    stats = player["stats"]
    equipment = player["equipment"]

    if action["arg3"] == A_SPECIFIC:
        if action["arg4"] == B_NORTH:
            action["arg1"] = location["x"]
            action["arg2"] = location["y"] + doMaxMove(player)
        elif action["arg4"] == B_NORTH_EAST:
            action["arg1"] = location["x"] + doAngleMove(player)
            action["arg2"] = location["y"] + doAngleMove(player)
        elif action["arg4"] == B_EAST:
            action["arg1"] = location["x"] + doMaxMove(player)
            action["arg2"] = location["y"]
        elif action["arg4"] == B_SOUTH_EAST:
            action["arg1"] = location["x"] + doAngleMove(player)
            action["arg2"] = location["y"] - doAngleMove(player)
        elif action["arg4"] == B_SOUTH:
            action["arg1"] = location["x"]
            action["arg2"] = location["y"] - doMaxMove(player)
        elif action["arg4"] == B_SOUTH_WEST:
            action["arg1"] = location["x"] - doAngleMove(player)
            action["arg2"] = location["y"] - doAngleMove(player)
        elif action["arg4"] == B_WEST:
            action["arg1"] = location["x"] - doMaxMove(player)
            action["arg2"] = location["y"]
        elif action["arg4"] == B_NORTH_WEST:
            action["arg1"] = location["x"] - doAngleMove(player)
            action["arg2"] = location["y"] + doAngleMove(player)

    print(action["arg1"])
    print(action["arg2"])

    if action["arg3"] == A_NEAR:
        action["arg1"] = location["x"]
        action["arg2"] = location["y"]
        x, y = doMoveClose(action["arg1"], action["arg2"], doMaxMove(player))
    elif action["arg3"] == A_FAR:
        action["arg1"] = sgn(location["x"]) * (D_CIRCLE + fabs(location["x"])) * (2 * random() + 2)
        action["arg2"] = sgn(location["y"]) * (D_CIRCLE + fabs(location["y"])) * (2 * random() + 2)
    elif action["arg3"] == A_TRANSPORT:
        x, y = doMoveClose(0, 0, 2000 * random())

        # use whichever x is larger of old and new
        if fabs(location["x"]) > fabs(x):
            action["arg1"] = location["x"]
        else:
            action["arg1"] = x
        # use whichever y is larger of old and new
        if fabs(location["y"]) > fabs(y):
            action["arg2"] = location["y"]
        else:
            action["arg2"] = y

    elif action["arg3"] == A_OUST:
        x, y = doMoveClose(0, 0, 5000 * random())

        # use whichever x is larger of old and new
        if fabs(location["x"]) > fabs(x):
            action["arg1"] = location["x"]
        else:
            action["arg1"] = x
        # use whichever y is larger of old and new
        if fabs(location["y"]) > fabs(y):
            action["arg2"] = location["y"]
        else:
            action["arg2"] = y
    elif action["arg3"] == A_BANISH:
        action["arg1"] = location["x"]
        action["arg2"] = location["y"]
        if fabs(location["x"]) > fabs(location["y"]):
            if (fabs(location["x"]) < D_BEYOND):
                action["arg1"] = sgn(location["x"]) * D_BEYOND
        else:
            if (fabs(location["y"]) < D_BEYOND):
                action["arg2"] = sgn(location["y"]) * D_BEYOND;

    action["arg1"] = floor(action["arg1"])
    action["arg2"] = floor(action["arg2"])

    """
	# check to make sure there are no it_combat events not received */
    if (Do_check_encountered(c)):
	    Do_unlock_mutex(&c->realm->realm_lock)
	    c->stuck = TRUE
	    return
    """

	# the move is successful - handle any events in the queue
	# only orphan events if the player is leaving the square -
	# this closes the king safe send through deliberate itcombat

    #if (the_event->arg1 != c->player.x || the_event->arg2 != c->player.y)
	#    Do_orphan_events(c);

    # if returning from beyond
    if (action["arg3"] != A_FORCED and location["beyond"] and \
	    fabs(action["arg1"]) < D_BEYOND and fabs(action["arg2"]) < D_BEYOND):
        if fabs(location["x"]) > fabs(location["y"]):
            action["arg1"] = sgn(location["x"]) * D_BEYOND
        else:
            action["arg2"] = sgn(location["y"]) * D_BEYOND

    location["beyond"] = False
    # see if the player is beyond
    if fabs(action["arg1"]) >= D_BEYOND or fabs(action["arg2"]) >= D_BEYOND:
        location["beyond"] = False
    # if moving off the board's edge
    if fabs(action["arg1"]) >= D_EDGE or fabs(action["arg2"]) >= D_EDGE:
	    # stop a character at the edge
	    # send over if they move that way again
        if fabs(action["arg1"]) >= D_EDGE or fabs(action["arg2"]) >= D_EDGE:
            if location["location"] == PL_EDGE and (action["arg3"] == A_SPECIFIC or action["arg3"] == A_TELEPORT):
                newEvent = newEvent(DEATH_EVENT, 0, 0, K_FELL_OFF)
                print("DEAD!")
            location["location"] = PL_EDGE
            if fabs(action["arg1"]) > D_EDGE:
                action["arg1"] = sgn(action["arg1"]) * D_EDGE
            if abs(action["arg2"]) > D_EDGE:
                action["arg2"] = sgn(action["arg2"]) * D_EDGE
        else:
            location["location"]  = PL_REALM

    # see if we're in the throne room
    #cursor = db.session.execute("SELECT player_id, king_flag, x, y FROM king")
    #king=cursor.fetchone()
    #print(king)
    #king_flag = False
    #if action["arg1"] == 0 and action["arg2"] == 0:
    #    if status["special_type"] == SC_STEWARD or status["special_type"] == SC_KING:
    #        return
    #    if stats["level"] >= 10 or stats["level"] <= 200:
    #        if equipment["crowns"] > 0:
    #            if not king_flag:
    #                location["location"] = PL_THRONE

    location["x"] = action["arg1"]
    location["y"] = action["arg2"]
    # dispose of the action
    del payload["action"]

def doMaxMove(player):

    circle = player["location"]["circle"]
    level = player["stats"]["level"]
    if circle > 19 and circle < 36:
        return int(min(ceil(level / 50.0) + 1.5, 10.0))
    else:
        return int(min(floor((level * 1.5) + 1.5), 100.0))

def doAngleMove(player):
    return int(max(1.0, floor(doMaxMove(player) * .707106781)))
