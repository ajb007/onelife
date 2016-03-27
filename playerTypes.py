import json
from macros import roll
import move
from constants import D_CIRCLE

playerTypes = ""
playerType = ""

def init():
    global playerType
    global playerTypes
    with open("data/playerTypes.json") as data_file:
        data = json.load(data_file)
    playerTypes = data["playerTypes"]

def getPlayerType(type):
    global playerType
    global playerTypes
    for playerType in playerTypes:
        if playerType["name"] == type:
            return playerType

def rollPlayerType(type):

    newPlayer = []

    playerType = getPlayerType(type)
    stats = playerType["stats"][0]

    newPlayer.append({
      "type":type,
      "abbrv":stats["abbrv"],
      "energy":roll(stats["energy"]["base"], stats["energy"]["interval"]),
      "strength":roll(stats["strength"]["base"], stats["strength"]["interval"]),
      "quickness":roll(stats["quickness"]["base"], stats["quickness"]["interval"]),
      "magicLvl":roll(stats["magicLvl"]["base"], stats["magicLvl"]["interval"]),
      "mana":roll(stats["mana"]["base"], stats["mana"]["interval"]),
      "brains":roll(stats["brains"]["base"], stats["brains"]["interval"]),
      "gold":roll(stats["gold"]["base"], stats["gold"]["interval"]),
      "experience":roll(stats["experience"]["base"], stats["experience"]["interval"])
    })

    newPlayer.append(move.moveClose(0, 0, D_CIRCLE - 1))
    return newPlayer
