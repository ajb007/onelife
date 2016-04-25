import traceback
from flask import jsonify
from messages import message
from random import random
from math import floor, pow, sqrt
from macros import roll
from event import newEvent, stackEvent
import copy
from stats import (
    getPlayerType, doGems, doGold, doEnergy, doSpeed, doMana, doAdjustedPoison,
    doSin, doExperience
    )
from constants import (
    MESSAGE_MORE, MESSAGE_CLEAR, MESSAGE_YES, MESSAGE_NO, MESSAGE_YESNO, MESSAGE_YESNO_NOALL,
    D_BEYOND, MONSTER_EVENT, MONSTER_SPECIFY
    )
from app import db
from models import Objects
from misc import doDistance, doDirection

def doTreasure(payload):
    player = payload["player"]
    event = payload["reaction"]
    location = player["location"]

    # make a mutable copy of the current event. We will need it back after client response
    cpEvent = copy.deepcopy(event)
    # Gold and gems only in circles that aren't fully beyond
    if ((event["arg2"] == 10) or ((location["circle"] <= D_BEYOND / 88.388 and random() > 0.65) and not(event["arg2"] > 0))):
        if event["arg3"] > 7:
            # gems
            gems = floor(roll(1.0, pow(event["arg3"] - 7.0, 1.8) * (event["arg1"] - 1.0) / 4.0))
            if gems == 1:
                message(player, ["You have discovered a gem!\n"])
                message(player, ["Do you want to pick it up?\n", MESSAGE_YESNO])
            else:
                message(player, ["You have discovered %.0lf gems!\n" % gems])
                message(player, ["Do you want to pick them up?\n", MESSAGE_YESNO])
            event["message"] = {"type":"gems","gems":gems,"callback":"_answerGems","event":cpEvent}
        else:
            # gold
            gold = floor(roll(event["arg3"] * 10.0, event["arg3"] * event["arg3"] * 8.0 * (event["arg1"] - 1.0)))
            if gold == 1:
                gold = 2
            message(player, ["You have found %.0lf gold pieces.\n" % gold])
            message(player, ["Do you want to pick them up?\n", MESSAGE_YESNO])
            event["message"] = {"type":"gold","gold":gold,"callback":"_answerGold","event":cpEvent}
    else:
        # Other treasure
        message(player, ["You have found some treasure. Do you want to inspect it?\n", MESSAGE_YESNO_NOALL])
        event["message"] = {"type":"other","callback":"_answerOther","event":cpEvent}

def _answerGems(payload):
    print("Calling _answerGems")
    player = payload["player"]
    action = payload["action"]
    event = action["message"]["event"]
    if random() < event["arg3"] / 35.0 + 0.04:
        if action["message"]["gems"] == 1:
            message(player, ["It was cursed!\n", MESSAGE_MORE, MESSAGE_CLEAR])
            doCursedTreasure(payload)
        else:
            message(player, ["They were cursed!\n", MESSAGE_MORE, MESSAGE_CLEAR])
            doCursedTreasure(payload)
    else:
        doGems(payload["player"], action["message"]["gems"], False)
        message(player, ["", MESSAGE_CLEAR])

def _answerGold(payload):
    print("_answerGold")
    player = payload["player"]
    action = payload["action"]
    event = action["message"]["event"]
    if random() < event["arg3"] / 35.0 + 0.04:
        # Never a single gold piece
        message(player, ["They were cursed!\n", MESSAGE_MORE, MESSAGE_CLEAR])
        doCursedTreasure(payload)
    else:
        doGold(payload["player"], action["message"]["gold"], False)
        message(player, ["", MESSAGE_CLEAR])

def _answerOther(payload):
    print("_answerOther")

    druidmesg = [
        "\tA blessing works perfectly if the bearer is free of any sin.\n",
        "\tA palantir can even pierce a cloak.\n",
        "\tA smurf berry a day keeps the medic away.\n",
        "\tA thaumaturgist can really put you in hot water!\n",
        "\tAll or nothing is your best friend against higher-level players.\n",
        "\tAmulets protect you from cursed treasure.\n",
        "\tBe careful to keep your sin low, or you may find yourself having a smurfy time.\n",
        "\tBe sure to rest if your speed drops from fatigue.\n",
        "\tBeware the Cracks of Doom!\n",
        "\tBeware the Jabberwock, my friend!  The jaws that bite, the claws that catch!\n",
        "\tBlindness wears off eventually... eventually.\n",
        "\tBuy amulets to protect your charms from being used on treasure.\n",
        "\tCatching a unicorn requires the virtue and control of a saint.\n",
        "\tDo not meddle in the affairs of the Game Wizards, for they are subtle and quick to anger.\n",
        "\tDo not ask to speak to a Game Wizard without giving your reason up front, or he will ignore you.\n",
        "\tDon't beg the Game Wizards for help with the game.\n",
        "\tDon't swear on channel 1.  Acronyms count, too.\n",
        "\tDwarves regenerate energy faster than other characters.\n",
        "\tElves are immune to the plague!\n",
        "\tExperimentos have been known to come back from the dead!\n",
        "\tFighting the Dark Lord leads to certain death...unless it's a Mimic!\n", "\tHalflings are said to be extremely lucky.\n",
        "\tIf the game isn't acting the way it should, report it to an Apprentice.\n",
        "\tIf your speed drops a lot, get rid of some of the heavy gold you are carrying.\n",
        "\tIt doesn't matter if you buy books one at a time or all at once.\n",
        "\tIt is impossible to teleport into the Dead Marshes except via the eagle Gwaihir.\n",
        "\tIt is very hard to walk through the Dead Marshes.\n",
        "\tKeep moving farther out, or you'll die from old age.\n",
        "\tListen to the Apprentices, they speak with the voice of the Game Wizards.\n",
        "\tMedics don't like liars, and punish accordingly.\n",
        "\tMedics don't work for charity.\n",
        "\tMerchants don't like players sleeping on their posts.\n",
        "\tOnly a moron would fight morons for experience.\n",
        "\tOnly a fool would dally with a Succubus or Incubus.\n",
        "\tOnly the Steward can give gold, but beware their smurfs if you ask too many times!\n",
        "\tParalyze can be a slow character's best friend.\n",
        "\tPicking up treasure while poisoned is bad for your health.\n",
        "\tReading the rules is a very good idea, and is often rewarded.\n",
        "\tRings of power contain much power, but much peril as well.\n",
        "\tSaintly adventurers may not have as much fun, but they tend to live longer.\n",
        "\tSmurfs may look silly, but they are actually quite deadly.\n",
        "\tStockpile amulets to protect your charms.\n",
        "\tTeleports are more efficient over short distances.\n",
        "\tThe corpse of a councilmember or a valar has never been found.\n",
        "\tThe One Ring is most likely to be found in the Cracks of Doom.\n",
        "\tThere are only three certainties in Phantasia : death, taxes, and morons.\n",
        "\tThe Game Wizards are always right.\n",
        "\tThe gods will revoke their blessing if you sin too much.\n",
        "\tThe nastier your poison, the more gold a medic will want to cure it.\n",
        "\tThere is a post in the Plateau of Gorgoroth that sells blessings.\n",
        "\tWant to live dangerously?  Nick a shrieker.\n",
        "\tWhen all else fails ... use all or nothing.\n",
        "\tWhen starting, do not spend too much money at once, or you may be branded a thief.\n",
        "\tWizards have been known to be nice if you are polite without being obsequious.\n",
        ]

    player = payload["player"]
    action = payload["action"]
    event = action["message"]["event"]
    equipment = player["equipment"]
    stats = player["stats"]
    battle = player["battle"]
    status = player["status"]

    # make a mutable copy of the current event. We will need it back after client response
    cpEvent = copy.deepcopy(event)

    if random() < 0.08 and event["arg3"] != 4:
        message(player, ["It was cursed!\n", MESSAGE_MORE, MESSAGE_CLEAR])
        doCursedTreasure(payload)
    else:
        if event["arg2"] > 0 and event["arg2"] < 4:
            whichtreasure = event["arg2"]
        else:
            # pick a treasure
            whichtreasure = int(roll(1.0, 3.0))
        if event["arg3"] == 1:
            # Treasure Type 1
            if whichtreasure == 1:
                message(player, ["You've found a vial of holy water!\n", MESSAGE_MORE, MESSAGE_CLEAR])
                equipment["holy_water"] += 1
            elif whichtreasure == 2:
                dtemp = floor(sqrt(event["arg1"]))
                if dtemp < 1:
                    dtemp = 1
                if dtemp == 1:
                    message(player, ["You've found an amulet of protection.\n", MESSAGE_MORE, MESSAGE_CLEAR])
                else:
                    message(player, ["You've found %.0lf amulets of protection.\n" % dtemp, MESSAGE_MORE, MESSAGE_CLEAR])
                equipment["amulets"] += dtemp
            elif whichtreasure == 3:
                message(player, ["You have found a holy orb. You feel less sinful.\n", MESSAGE_MORE, MESSAGE_CLEAR])
                doSin(player, -0.1)
        elif event["arg3"] == 2:
            # Treasure Type 2
            if whichtreasure == 1:
                if stats["sin"] < 9.5 * random() + 0.5:
                    message(player, ["You have encountered a druid who teaches you the following words of wisdom:\n"])
                    message(player, [druidmesg[int(roll(0.0, len(druidmesg)))], MESSAGE_MORE, MESSAGE_CLEAR])
                    doExperience(player, roll(0.0, 2000.0 + event["arg1"] * 750.0), False)
                else:
                    message(player, ["You have encountered a druid.  He runs in fear for his life!\n", MESSAGE_MORE, MESSAGE_CLEAR])
            elif whichtreasure == 2:
                dtemp = floor((.5 + random()) * 15 * event["arg1"])
                message(player, ["You've found a +%.0lf buckler.\n" % dtemp])
                if dtemp >= equipment["shield"]:
                    message(player, ["", MESSAGE_MORE, MESSAGE_CLEAR])
                    doEnergy(player, stats["energy"] - equipment["shield"] +
                        dtemp, stats["max_energy"], dtemp, 0, False)
                else:
                    message(player, ["But you already have something better.\n"])
                message(player, ["", MESSAGE_MORE, MESSAGE_CLEAR])
            elif whichtreasure == 3:
                if stats["poison"] > 0.0:
                    doAdjustedPoison(player, -0.25)
                    if stats["poison"] < 0.0:
                        stats["poison"] = 0.0
                        message(player, ["You've found some smurf berries!  You feel cured!\n", MESSAGE_MORE, MESSAGE_CLEAR])
                    else:
                        message(player, ["You've found some smurf berries!  You feel slightly better.\n", MESSAGE_MORE, MESSAGE_CLEAR])
                else:
                    message(player, ["You've found some smurf berries!  You feel smurfy!\n", MESSAGE_MORE, MESSAGE_CLEAR])

                battle["rounds"] /= 2
                doSpeed(player, stats["max_quickness"], equipment["quicksilver"], 0, False)
                doEnergy(player, stats["energy"] + (stats["max_energy"] + equipment["shield"]) / 15.0 + stats["level"] / 3.0 + 2.0,
                    stats["max_energy"], equipment["shield"], battle["force_field"], False)
        elif event["arg3"] == 3:
            # Treasure type 3
            if whichtreasure == 1:
                message(player, ["You've met a hermit!  You heal, gain mana, and lose sin.\n", MESSAGE_MORE, MESSAGE_CLEAR])

                if stats["sin"] > 6.66:
                    doSin(player, -1.0)
                else:
                    doSin(player, -0.15 * stats["sin"])
                ptype = getPlayerType(status["type"])["stats"][0]
                doMana(player, ptype["mana"]["increase"] / 2 * event["arg1"], False)
                doEnergy(player, stats["energy"] + (stats["max_energy"] + equipment["shield"]) / 7.0 + stats["level"] / 3.0 + 2.0,
                    stats["max_energy"], equipment["shield"], battle["force_field"], False)
            elif whichtreasure == 2:
                message(player, ["You've found a virgin but we will sort her out later ... \n", MESSAGE_MORE, MESSAGE_CLEAR])
            elif whichtreasure == 3:
                dtemp = floor((.5 + random()) * event["arg1"])
                if dtemp < 1:
                    dtemp = 1
                message(player, ["You've found a +%.0lf short sword!\n" % dtemp])
                if dtemp >= equipment["sword"]:
                    doStrength(player, stats["max_strength"], dtemp, 0, False)
                else:
                    message(player, ["But you already have something better.\n"])
                message(player, ["", MESSAGE_MORE, MESSAGE_CLEAR])
        elif event["arg3"] == 4:
            # Treasure type 4
            if status["blind"]:
                message(player, ["You've found a scroll.  Too bad you are blind!\n", MESSAGE_MORE, MESSAGE_CLEAR])
            else:
                message(player, ["You've found a scroll.  Will you read it?\n", MESSAGE_YESNO])
                # We need to stack the event here otherwise we lose the event
                readEvent = newEvent(event["type"], event["arg1"], event["arg2"], event["arg3"], "")
                readEvent["message"] = {"type":"other","callback":"_answerReadScroll", "event":cpEvent}
                stackEvent(payload, readEvent)

    #message(player, ["", MESSAGE_CLEAR])

def _answerReadScroll(payload):

    print("_answerReadScroll")

    player = payload["player"]
    action = payload["action"]
    event = action["message"]["event"]
    stats = player["stats"]
    status = player["status"]
    currency = player["currency"]

    if event["arg2"] > 0 and event["arg2"] < 7:
        dtemp = event["arg2"]
    else:
        # pick a scroll type
        dtemp = int(roll(1, 6))

    if dtemp == 1:
        print(stats["level"])
        if stats["level"] <= 100 - currency["gems"]:
            doTreasureMap(payload)
    else:
        # character is too high level, pick another scroll
        dtemp = int(roll(2, 5))

        if dtemp == 2:
            message(player, ["It throws up a shield for your next monster.\n", MESSAGE_MORE, MESSAGE_CLEAR])
            status["shield_nf"] += 1
        if dtemp == 3:
            message(player, ["It makes you faster for your next monster.\n", MESSAGE_MORE, MESSAGE_CLEAR])
            status["haste_nf"] += 1
        if dtemp == 4:
            message(player, ["It increases your strength for your next monster.\n", MESSAGE_MORE, MESSAGE_CLEAR])
            status["strong_nf"] += 1
        if dtemp == 5:
            message(player, ["It tells you how to pick your next monster.\n", MESSAGE_MORE, MESSAGE_CLEAR])
            pickEvent = newEvent(MONSTER_EVENT, MONSTER_SPECIFY, 0, 0, "")
            stackEvent(payload, pickEvent)
        if dtemp == 6:
            message(player, ["It was cursed!\n", MESSAGE_MORE, MESSAGE_CLEAR])
            doCursedTreasure(payload)

def doTreasureMap(payload):
    print("doTreasureMap")

    player = payload["player"]
    location = player["location"]

    trove = Objects.query.filter(Objects.object_type == "TROVE").all()

    x_loc = trove[0].x
    y_loc = trove[0].y

    # determine the distance to the trove
    dtemp = doDistance(location["x"], x_loc, location["y"], y_loc)
    if dtemp > 1.0:
        # throw in a fudge factor of up to 12.5% if not near trove
        dtemp = floor(dtemp * (.875 + random() * .25) + .01)
        msg = "It says, 'To find me treasure trove, ye must move %.0lf squares to the " % dtemp
        msg = msg + doDirection(player, x_loc, y_loc)
        msg = msg + " and then look for me next map.\n"
        message(player, [msg, MESSAGE_MORE, MESSAGE_CLEAR])
    elif dtemp == 1.0:
        msg = "Arr, you're almost there.  The booty is 1 square "
        msg = msg + doDirection(player, x_loc, y_loc)
        message(player, [msg, MESSAGE_MORE, MESSAGE_CLEAR])
    else:
        message(player, ["You've found the treasure!  Dig matey, dig!\n", MESSAGE_MORE, MESSAGE_CLEAR])

def doCursedTreasure(payload):

    player = payload["player"]
    location = player["location"]
    equipment = player["equipment"]
    stats = player["stats"]
    status = player["status"]

    if equipment["amulets"] >= floor(sqrt(location["circle"])):
        message(player, ["But your amulets saved you!\n", MESSAGE_MORE])
        equipment["amulets"] -= floor(sqrt(location["circle"]))
    elif equipment["charms"] > 0:
        message(player, ["But your charm saved you!\n", MESSAGE_MORE])
        equipment["charms"] = equipment["charms"] - 1
    else:
        message(player, ["", MESSAGE_MORE])
        dtemp = stats["energy"] - random() * (stats["max_energy"] + equipment["shield"]) / 3.0
        if dtemp < stats["max_energy"] / 10.0:
            dtemp = min(stats["energy"], stats["max_energy"] / 10.0)
        doEnergy(player, dtemp, stats["max_energy"], equipment["shield"], 0, False)
        doAdjustedPoison(player, 0.25)

    message(player, ["", MESSAGE_CLEAR])
