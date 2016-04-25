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

def stackEvent(payload, event):
    if not "events" in payload.keys():
        payload["events"] = []
    payload["events"].append(event)

def nextEvent(payload):
    reaction = payload["events"][0]
    del payload["events"][0]
    return reaction

def cancelTreasureEvents(payload):
    if "events" in payload.keys():
        events = payload["events"]
        i = len(events)-1
        while True:
            if i < 0:
                break
            event = events[i]
            if event["type"] == TREASURE_EVENT:
                del events[i]
            i -= 1

def randomEvent(payload):

    event = {}

    event["type"] = NULL_EVENT
    event["arg1"] = 0
    event["arg2"] = 0
    event["arg3"] = 0
    event["message"] = ""

    # MORON event if speed is 0
    if payload["player"]["stats"]["quickness"] == 0 and random() >= .1 * payload["player"]["stats"]["degenerated"]:
        event["type"] = MONSTER_EVENT
        event["arg1"] = MONSTER_RANDOM
        event["arg3"] = 16
        return event

    if payload["player"]["status"]["blind"] == True and random() <= 0.0075:
        event["message"] = "You've regained your sight!"
        player["status"]["blind"] == False
        return event

    if random() <= 0.0133:
        event["type"] = MEDIC_EVENT
        return event

    if random() <= 0.0075:
        event["type"] = GURU_EVENT
        return event

    if random() <= 0.005:
        event["type"] = PLAGUE_EVENT
        return event

    if random() <= 0.0075:
        event["type"] = VILLAGE_EVENT
        return event

    if payload["player"]["stats"]["level"] < 3000:
        if random() <= 0.0033 + payload["player"]["stats"]["level"] * .00000125:
            event["type"] = TAX_EVENT
            return event
        elif random() <= 0.0033:
            event["type"] = TAX_EVENT
            return event

    if random() <= 0.015:
        event["type"] = TREASURE_EVENT
        event["arg1"] = payload["player"]["location"]["circle"]
        event["arg3"] = 1
        return event

    if random() <= 0.0075:
        event["type"] = TREASURE_EVENT
        event["arg1"] = payload["player"]["location"]["circle"]
        event["arg3"] = 2
        return event

    if random() <= 0.20:
        event["type"] = MONSTER_EVENT
        event["arg1"] = MONSTER_RANDOM
        event["arg3"] = SM_RANDOM
        return event

    return event

def monsterInBattleEvent(payload):
    battle = payload["player"]["battle"]

    event = {}

    event["type"] = MONSTER_EVENT
    event["arg1"] = MONSTER_RANDOM
    event["arg3"] = battle["opponent"]["type"]
    return event

def handleEvent():
    # handle any incoming events
    a = 1
