from macros import roll
from random import random
from math import floor, sqrt
from stats import doEnergy, doSin
import json
import numpy
from constants import (
    C_EXPER,
    NUM_MONSTERS,
    MONSTER_RANDOM,
    MONSTER_CALL,
    MONSTER_FLOCKED,
    MONSTER_SHRIEKER,
    MONSTER_JABBERWOCK,
    MONSTER_SPECIFY,
    MONSTER_SUMMONED,
    MONSTER_TRANSFORM,
    MONSTER_PURGATORY,
    SC_COUNCIL,
    SC_VALAR,
    SC_EXVALAR,
    R_DLREG,
    R_NONE,
    SM_CERBERUS,
    SM_JABBERWOCK,
    SM_MODNAR,
    SM_MORGOTH,
    SM_MIMIC,
    SM_SUCCUBUS,
    SM_UNICORN,
    SM_DARKLORD,
    SM_MORON,
    N_SWORDPOWER,
    SM_IT_COMBAT
)

def rollMonster(payload):

    player = payload["player"]
    main = player["main"]
    equipment = player["equipment"]
    location = player["location"]
    status = player["status"]
    stats = player["stats"]
    event = payload["reaction"]

    s = stats["strength"]

    with open("data/monsters.json") as data_file:
        monsters_json = json.load(data_file)

    monsters = monsters_json["monsters"]

    firsthit = equipment["blessing"]  #set if player gets the first hit
    monsthit = True
    count = 0
    string_buffer = ""
    string_buffer2 = ""
    sTemp = 0
    dTemp = 0.0

    battle = {}
    battle["ring_in_use"] = False
    battle["tried_luckout"] = False
    battle["melee_damage"] = 0.0
    battle["skirmish_damage"] = 0.0
    battle["introduction"] = ""
    battle["force_field"] = False
    battle["messages"] = []
    battle["opponent"] = {}

    opponent = battle["opponent"]
    opponent["sin"] = 5

    if event["arg3"] >= 0 and event["arg3"] < NUM_MONSTERS:
        opponent["type"] = event["arg3"]

    else:
        if status["special_type"] == SC_VALAR:
            # even chance of any monster
            opponent["type"] = int(roll(0.0, 100.0))
        elif equipment["shield"] / stats["degenerated"] > 50000.0 and location["circle"] >= 36 and random() < 0.1:
            #  10% of getting cerbed with big shield
            opponent["type"] = 96
        elif equipment["quicksilver"] / stats["degenerated"] > 500.0 and location["circle"] >= 36 and random() < 0.1:
            # 10% of getting jabbed with big quick
            opponent["type"] = 94
        elif location["circle"] >= 36:
            #even chance of all non-water monsters
            opponent["type"] = int(roll(14.0, 86.0))
        elif location["circle"] == 27 or location["circle"] == 28:
            # the cracks of doom - no weak monsters except modnar
            opponent["type"] = int(roll(50.0, 50.0))
            # less than a unicorn then default to modnar
            if opponent["type"] < 52:
                opponent["type"] = 15
        elif location["circle"] < 31 and location["circle"] > 24:
            # gorgoroth - no weak monsters except modnar weighed towards middle
            opponent["type"] = int(roll(50.0, 25.0) + roll(00.0, 26.0))
            # less than a unicorn then default to modnar
            if opponent["type"] < 52:
                opponent["type"] = 15
        elif location["circle"] > 19:
            # the marshes - water monsters, idiots, and modnar
            opponent["type"] = int(roll(00.0, 17.0))
        elif location["circle"] > 15:
            # chance of all non-water monsters, weighted toward middle
            opponent["type"] = int(roll(00.0, 50.0) + roll(14.0, 37.0))
        elif location["circle"] > 9:
            # TT 1-8 monsters, weighted toward middle
            opponent["type"] = int(roll(0.0, (-8.0 + location["circle"] * 4)) + roll(14.0, 26.0))
        elif location["circle"] > 7:
            # Hard type 3-5 monsters
            opponent["type"] = int(roll(14.0, (18.0 + location["circle"] * 4)))
        elif location["circle"] > 4:
            # even chance of type 1-3 + easy type 4-5 monsters
            opponent["type"] = int(roll(14.0, 46.0))
        elif location["circle"] == 4:
            # even chance of all type 1-3
            opponent["type"] = int(roll(14.0, 38.0))
        else:
            # circle 1 -3
            # even chance of some of the tamest non-water monsters
            opponent["type"] = int(roll(14.0, (17.0 + location["circle"] * 4)))

    if opponent["type"] == 100:
        opponent["type"] = 15

    # determine monster size
    if event["arg2"] > 0:
        opponent["size"] = event["arg2"]
    elif location["circle"] == 27 or location["circle"] == 28:
        # cracks and gorgoroth scale with player level
        if equipment["ring_type"] == R_DLREG:
            opponent["size"] = max(location["circle"], floor((.2 + .3 * random()) * stats["level"]))
        if equipment["ring_type"] == R_NONE:
            opponent["size"] = max(location["circle"], floor((.15 + .35 * random()) * stats["level"]))
        else:
           opponent["size"] = max(location["circle"], floor((.1 + .25 * random()) * stats["level"]))
    elif location["circle"] < 31 and location["circle"] > 24:
        if equipment["ring_type"] == R_DLREG:
            opponent["size"] = max(location["circle"], floor((.15 + .1 * random()) * stats["level"]))
        if equipment["ring_type"] == R_NONE:
            opponent["size"] = max(location["circle"], floor((.1 + .15 * random()) * stats["level"]))
        else:
           opponent["size"] = max(location["circle"], floor((.05 + .1 * random()) * stats["level"]))
    else:
        opponent["size"] = location["circle"]

    monster = monsters[opponent["type"]]["monster"]
    opponent["name"] = monster["name"]
    opponent["real_name"] = monster["name"]
    opponent["experience"] = opponent["size"] * monster["experience"]
    opponent["brains"] = opponent["size"] * monster["brains"]
    opponent["strength"] = (1 + (opponent["size"] / 2)) * monster["strength"]
    opponent["max_strength"] = opponent["strength"]
    # Randomize energy slightly
    opponent["energy"] = floor(opponent["size"] * monster["energy"] * (0.9 + random() * 0.2))
    opponent["max_energy"] = opponent["energy"]
    opponent["speed"] = opponent["size"] * monster["speed"]
    opponent["max_speed"] = opponent["speed"]
    opponent["special_type"] = monster["special_type"]
    opponent["treasure_type"] = monster["treasure_type"]
    opponent["flock_percent"] = monster["flock_percent"]
    opponent["shield"] = 0.0

    # handle some special monsters
    if opponent["special_type"] == SM_MODNAR:
        if status["special_type"] < SC_COUNCIL:
            opponent["strength"] *= floor(random() + 0.5)
            opponent["brains"] *= floor(random() + 0.5)
            opponent["speed"] *= floor(random() + 0.5)
            opponent["energy"] *= floor(random() + 0.5)
            opponent["experience"] *= floor(random() + 0.5)
            opponent["treasure_type"] = roll(0.0, opponent["treasure_type"])
        else:
            # make Modnar into Morgoth */
            opponent["name"] = "Morgoth"
            opponent["real_name"] = "Morgoth"
            opponent["special_type"] = SM_MORGOTH;

            opponent["energy"] = opponent["max_energy"] = \
                floor((8 + (stats["level"] / 250)) *
                (stats["strength"] *
                (1 + sqrt(equipment["sword"]) * N_SWORDPOWER)) *
                (0.75 + random() * 0.5))

            opponent["strength"] = opponent["max_strength"] = \
                floor((.025 + random() * ((.02 + .05 * stats["level"]/10000))) *
                (stats["max_energy"] + equipment["shield"]))

            if status["special_type"] == SC_EXVALAR:
                opponent["speed"] = 1
            elif random() < 0.5:
                opponent["speed"] = 1 + random() * ((stats["level"] - 2500) / 7500)
            else:
                opponent["speed"] = 1 - random() * ((stats["level"] - 2500) / 7500)

            opponent["speed"] *= stats["max_quickness"] + sqrt(equipment["quicksilver"]) - opponent["size"] * .0005;

			# Morgie gets faster as you go on to counter stat balancing */
            if stats["level"] >= 3000 and stats["level"] < 4000:
                opponent["max_speed"] = opponent["speed"]
            elif stats["level"] >= 4000 and stats["level"] < 5000:
                opponent["max_speed"] = opponent["speed"]*1.05
            elif stats["level"] >= 5000 and stats["level"] < 6000:
                opponent["max_speed"] = opponent["speed"]*1.1
            elif stats["level"] >= 6000 and stats["level"] < 7000:
                opponent["max_speed"] = opponent["speed"]*1.15
            elif stats["level"] >= 7000 and stats["level"] < 8000:
                opponent["max_speed"] = opponent["speed"]*1.2
            elif stats["level"] >= 8000 and stats["level"] < 9000:
                opponent["max_speed"] = opponent["speed"]*1.25
            elif stats["level"] >= 9000 and stats["level"] < 10000:
                opponent["max_speed"] = opponent["speed"]*1.3
            else:
                opponent["max_speed"] = opponent["speed"]*1.35

            opponent["brains"] = stats["brains"] * 20
            opponent["flock_percent"] = 0.0
            # Morgoth drops gold to annoy players
            opponent["treasure_type"] = 7;
            opponent["experience"] = floor(opponent["energy"] / 4)
    elif opponent["special_type"] == SM_MIMIC:
        # pick another name */
        print(opponent["name"])
        while (opponent["name"] == "A Mimic"):
            print("Here")
            opponent["name"] = monsters[int(roll(0.0, 100.0))]["monster"]["name"]
        print(opponent["name"])
        if opponent["name"] == "A Succubus" and stats["gender"] == "Female":
            opponent["name"] ==  "An Incubus"

        firsthit = True
    elif opponent["special_type"] == SM_SUCCUBUS and stats["gender"] == "Female":
        #females should be tempted by incubi, not succubi
        opponent["name"] ==  "An Incubus"
        opponent["real_name"] == "An Incubus"

    if status["blind"]:
        opponent["name"] =  "A monster"
        event["arg1"] = MONSTER_RANDOM

    if opponent["special_type"] == SM_UNICORN:
        if equipment["virgin"]:
            if random() < stats["sin"] - .1:
                battle["introduction"] = "%s glares at you and gallops away with your virgin!\n" % opponent["name"]
                equipment["virgin"] = False
                opponent.clear()
                return payload, battle
            else:
                battle["introduction"] = "You just subdued %s, thanks to the virgin.\n" % opponent["name"]
                equipment["virgin"] = False
                opponent["energy"] = 0.0
        elif not status["blind"]:
            battle["introduction"] = "You just saw %s running away!\n" % opponent["name"]
            opponent.clear()
            return payload, battle
        else:
            battle["introduction"] = "You just heard %s running away!\n" % opponent["name"]
            opponent.clear()
            return payload, battle

    if opponent["special_type"] == SM_MORGOTH:
        battle["introduction"] = "You've encountered %s, Bane of the Council and Enemy of the Vala.\n" % opponent["name"]

    if opponent["special_type"] == SM_DARKLORD:
        if equipment["blessing"]:
            if equipment["charms"] >= floor(opponent["size"] * (.8 - .1 * status["type"])) + 1:
                battle["introduction"] = "You just overpowered %s!\n" % opponent["name"]
                equipment["charms"] -= max(floor(opponent["size"] * (.8 - .1 * status["type"])), \
                    floor((.35 - (.05 * status["type"])) * equipment["charms"]))
                if equipment["charms"] < 0:
                    equipment["charms"] = 0
                opponent["energy"] = 0.0
                battle["broadcast"] = "%s has just defeated %s!\n" % (main["name"], opponent["name"])
        print(equipment["charms"])

    # give this new monster the proper introduction
    if opponent["energy"] > 0:
        if event["arg1"] == MONSTER_RANDOM:
            battle["introduction"] = "You are attacked by %s." % opponent["name"]
        elif event["arg1"] == MONSTER_CALL:
            battle["introduction"] = "You find and attack %s." % opponent["name"]
        elif event["arg1"] == MONSTER_FLOCKED:
            battle["introduction"] = "%s's friend appears and attacks." % opponent["name"]
        elif event["arg1"] == MONSTER_SHRIEKER:
            battle["introduction"] = "%s responds to the shrieker's clamor." % opponent["name"]
        elif event["arg1"] == MONSTER_JABBERWOCK:
            battle["introduction"] = "The Jabberwock summons %s." % opponent["name"]
        elif event["arg1"] == MONSTER_TRANSFORM:
            battle["introduction"] = "%s now attacks." % opponent["name"]
        elif event["arg1"] == MONSTER_SUMMONED:
            battle["introduction"] = "%s appears and attacks." % opponent["name"]
        elif event["arg1"] == MONSTER_SPECIFY:
            battle["introduction"] = "%s appears and attacks." % opponent["name"]
        elif event["arg1"] == MONSTER_PURGATORY:
            battle["introduction"] = "%s appears and attacks." % opponent["name"]
            # Purgatory characters always get first attack since they
    		# had the turn when they disconnected
            firsthit = True
            # Assume they already lucked out
            battle["tried_luckout"] = True
            # prevent players from rerolling monster size
            if location["circle"] < 31 and location["circle"] > 24:
                battle["messages"].append("The monster appears to have grown stronger in your absence!\n")
                opponent["size"] = max(location["circle"], .5 * stats["level"])

        battle["introduction"] = battle["introduction"] + " - (Size: %.0f)\n" % opponent["size"]

	# allow experimentos to test the speed equation */

    if opponent["special_type"] == SM_MORON:
        if status["type"] == C_EXPER and stats["level"] == 0:
            opponent["speed"] = opponent["max_speed"] = stats["quickness"]
            battle["messages"].append("Recognizing a kindred spirit, A Moron now moves as quickly as you!\n")
            battle["messages"].append("You feel fully refreshed and healed for battle!\n")

            doEnergy(player, stats["max_energy"] + equipment["shield"],
                stats["max_energy"], equipment["shield"],
                battle["force_field"], False)
            battle["rounds"] = 0

    # This needs moving somewhere (originally from Client)
    morgothCount = 0

    # adjust equipment-stealing monsters to knock off unbalanced chars
    if opponent["special_type"] == SM_CERBERUS:
        if (equipment["shield"] / stats["degenerated"] > 100000.0) and stats["degenerated"] < 50:
            opponent["speed"] = stats["max_quickness"] * 4
            opponent["max_speed"] = opponent["speed"]
            battle["messages"].append("Cerberus's eyes flare brightly as he sees the immense amounts of metal you are carrying!\n")
    elif opponent["special_type"] == SM_JABBERWOCK:
        if (equipment["quicksilver"] / stats["degenerated"] > 500.0) and stats["degenerated"] < 50:
            opponent["speed"] = stats["max_quickness"] * 4
            opponent["max_speed"] = opponent["speed"]
            battle["messages"].append("A Jabberwock whiffles in delight as it sees your immense stash of quicksilver!\n")
    elif opponent["special_type"] == SM_DARKLORD:
        if equipment["blessing"] and opponent["energy"] > 0 and morgothCount == 0:
            battle["messages"].append("Your blessing is consumed by the great evil of your opponent!\n")
            equipment["blessing"] = False
        elif opponent["energy"] > 0 and morgothCount > 0:
            battle["messages"].append("The Dark Lord keeps a safe distance away from you, smelling the scent of its masters blood upon your sword!\n")

    opponent["special_type"] = SM_DARKLORD
    equipment["ring_type"] = R_DLREG
    equipment["blessing"] = True
    opponent["treasure_type"] = 100
    stats["sin"] = 100

    if equipment["ring_type"] > R_NONE:
        if opponent["special_type"] != SM_IT_COMBAT:
            tt = 1 if opponent["treasure_type"] == 0 else opponent["treasure_type"]
            if random() * 1000 / tt < stats["sin"]:
                battle["messages"].append("You feel compelled to put your ring on your finger!\n")
                battle["ring_in_use"] = True
                newMessages, newEvent = doSin(player, 0.1)
                print(newMessages)
                print(newEvent)
                # log "%s, %s, forced_ring.\n", lcname, class_name


    payload["battle"] = battle
