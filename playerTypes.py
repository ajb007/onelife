import json
from move import setCircle, setLocation, doMoveClose
from macros import roll, calcLevel
from constants import D_CIRCLE, PL_REALM
from stats import getPlayerType, doEnergy

def rollPlayerType(payload):

    newPlayer = payload["player"]

    newPlayer["messages"] = []

    main = newPlayer["main"]
    equipment = newPlayer["equipment"]
    location = newPlayer["location"]
    currency = newPlayer["currency"]
    status = newPlayer["status"]
    stats = newPlayer["stats"]

    playerType = getPlayerType(status["type"])
    newPlayerStats = playerType["stats"][0]

    location["location"] = PL_REALM
    setCircle(location)
    x, y = doMoveClose(0, 0, D_CIRCLE - 1)
    location["x"] = x
    location["y"] = y
    setLocation(location)
    stats["energy"] = roll(newPlayerStats["energy"]["base"], newPlayerStats["energy"]["interval"])
    stats["max_energy"] = stats["energy"]
    stats["strength"] = roll(newPlayerStats["strength"]["base"], newPlayerStats["strength"]["interval"])
    stats["max_strength"] = stats["strength"]
    stats["quickness"] = roll(newPlayerStats["quickness"]["base"], newPlayerStats["quickness"]["interval"])
    stats["max_quickness"] = stats["quickness"]
    stats["magic_level"] = roll(newPlayerStats["magic_level"]["base"], newPlayerStats["magic_level"]["interval"])
    stats["mana"] = roll(newPlayerStats["mana"]["base"], newPlayerStats["mana"]["interval"])
    stats["brains"] = roll(newPlayerStats["brains"]["base"], newPlayerStats["brains"]["interval"])
    currency["gold"] = roll(newPlayerStats["gold"]["base"], newPlayerStats["gold"]["interval"])
    stats["experience"] = roll(newPlayerStats["experience"]["base"], newPlayerStats["experience"]["interval"])
    stats["level"] = calcLevel(stats["experience"])
    stats["degenerated"] = 1

    doEnergy(newPlayer, stats["energy"], stats["energy"], 0.0, 0.0, False)

    #print(newPlayer)
    return payload
