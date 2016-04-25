from messages import message
from random import random
from constants import MESSAGE_NORMAL, MESSAGE_MORE, MESSAGE_CLEAR
from stats import doPoison, doMana, doEnergy
from math import sqrt, atan

def doDistance(x1, x2, y1, y2):

    deltax = x1 - x2
    deltay = y1 - y2

    return sqrt(deltax * deltax + deltay * deltay)

def doDirection(player, x, y):

    location = player["location"]

    # if we're on the X coordinate, get radians manually
    if x - location["x"] == 0:

        if y - location["y"] > 0:
            radians = 1.5708
        elif y - location["y"] < 0:
            radians = 4.7124
        else:
            return "down"
    else:

        # find the angle
        radians = atan((y - location["y"])/(x - location["x"]))

        # add 180 degrees if on the other side of the plane
        if (x - location["x"] < 0):
            radians += 3.1416;

    # run around the circle
    if radians > 4.3197:
        return "south"
    elif radians > 3.5343:
        return "south-west"
    elif radians > 2.7489:
        return "west"
    elif radians > 1.9635:
        return "north-west"
    elif radians > 1.1781:
        return "north"
    elif radians > .3927:
        return "north-east"
    elif radians > -.3927:
        return "east"
    elif radians > -1.1781:
        return "south-east"
    else:
        return "south"

def doGuru(payload):

    player = payload["player"]
    message(player, ["You've met a Guru. . .\n"])

    if random() * player["stats"]["sin"] > 1.0:
        message(player, ["You disgusted him with your sins!\n", MESSAGE_MORE, MESSAGE_CLEAR])
    elif player["stats"]["poison"] > 0.0:
        message(player, ["He looked kindly upon you, and cured you.\n", MESSAGE_MORE, MESSAGE_CLEAR])
        doPoison(player, -player["stats"]["poison"])
    elif random() / 10 > player["stats"]["sin"] and player["location"]["circle"] > 1:
        message(player, ["He slips something into your charm pouch as a reward for your saintly behavior!\n", MESSAGE_MORE, MESSAGE_CLEAR])
        doMana(player, 40.0 + 15 * player["location"]["circle"], False)
        player["equipment"]["charms"] += 1 + player["location"]["circle"] / 20
    else:
        message(player, ["He rewarded you for your virtue.\n", MESSAGE_MORE, MESSAGE_CLEAR])
        doMana(player, 40.0 + 10 * player["location"]["circle"], False)

        doEnergy(player, player["stats"]["energy"] + 2 + player["location"]["circle"] / 5, \
            player["stats"]["max_energy"], \
            player["equipment"]["shield"] + 2 + player["location"]["circle"] / 5, 0, False)
