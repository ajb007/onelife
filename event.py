# we will get smart with event, using redis queue or something similar
# current idea is to set up a queue for every player entering the realm
# for now, just generate a simple random event for every action
from random import random
from constants import (
    NULL_EVENT,
    MONSTER_EVENT,
    MONSTER_RANDOM,
    NULL_EVENT,
    MEDIC_EVENT,
    GURU_EVENT,
    PLAGUE_EVENT,
    VILLAGE_EVENT,
    TREASURE_EVENT,
    TAX_EVENT,
    SM_RANDOM
)

def newEvent(type, arg1, arg2, arg3, message):

    event = {}
    event["type"] = type
    event["arg1"] = arg1
    event["arg2"] = arg2
    event["arg3"] = arg3
    event["message"] = message

    return event


def randomEvent(player):

    newEvent = {}

    newEvent["type"] = NULL_EVENT
    newEvent["arg1"] = 0
    newEvent["arg2"] = 0
    newEvent["arg3"] = 0
    newEvent["message"] = ""

    if player["player"]["stats"]["quickness"] == 0 and random() >= .1 * player["player"]["stats"]["degenerated"]:
        newEvent["type"] = MONSTER_EVENT
        newEvent["arg1"] = MONSTER_RANDOM
        newEvent["arg3"] = 16
        return newEvent

    if player["player"]["status"]["blind"] == True and random() <= 0.0075:
        newEvent["message"] = "You've regained your sight!"
        player["status"]["blind"] == False
        return newEvent

    if random() <= 0.0133:
        newEvent["type"] = MEDIC_EVENT
        return newEvent

    if random() <= 0.0075:
        newEvent["type"] = GURU_EVENT
        return newEvent

    if random() <= 0.005:
        newEvent["type"] = PLAGUE_EVENT
        return newEvent

    if random() <= 0.0075:
        newEvent["type"] = VILLAGE_EVENT
        return newEvent

    if player["player"]["stats"]["level"] < 3000:
        if random() <= 0.0033 + player["player"]["stats"]["level"] * .00000125:
            newEvent["type"] = TAX_EVENT
            return newEvent
        elif random() <= 0.0033:
            newEvent["type"] = TAX_EVENT
            return newEvent

    if random() <= 0.015:
        newEvent["type"] = TREASURE_EVENT
        newEvent["arg1"] = player["player"]["location"]["circle"]
        newEvent["arg3"] = 1
        return newEvent

    if random() <= 0.0075:
        newEvent["type"] = TREASURE_EVENT
        newEvent["arg1"] = player["player"]["location"]["circle"]
        newEvent["arg3"] = 2
        return newEvent

    if random() <= 0.20:
        newEvent["type"] = MONSTER_EVENT
        newEvent["arg1"] = MONSTER_RANDOM
        newEvent["arg3"] = SM_RANDOM;
        return newEvent

    return newEvent
