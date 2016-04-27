from macros import roll
from random import random
from math import floor, sqrt, ceil, pow
from stats import (
    doEnergy, doSin, doSpeed, doMana, doExperience, doStrength,
    doPalantir, doGold, doGems, doScrambleStats, doAdjustedPoison, doRing
)
from event import newEvent, handleEvent, stackEvent
import json
import numpy
from messages import message, broadcast
from constants import (
    C_EXPER,C_HALFLING, C_DWARF, C_MAGIC,
    NUM_MONSTERS, MIN_KING,
    MONSTER_RANDOM, MONSTER_CALL, MONSTER_FLOCKED, MONSTER_SHRIEKER, MONSTER_JABBERWOCK,
    MONSTER_SPECIFY, MONSTER_SUMMONED, MONSTER_TRANSFORM, MONSTER_PURGATORY,
    SC_COUNCIL, SC_VALAR, SC_EXVALAR, SC_KING,
    R_DLREG, R_NAZREG, R_NONE, R_BAD, R_SPOILED,
    SM_CERBERUS, SM_JABBERWOCK, SM_MODNAR, SM_MORGOTH, SM_MIMIC, SM_SUCCUBUS,
    SM_UNICORN, SM_DARKLORD, SM_MORON, SM_SHRIEKER, SM_BALROG, SM_IT_COMBAT,
    SM_FAERIES, SM_TITAN, SM_SMURF, SM_IDIOT, SM_SMEAGOL, SM_TROLL, SM_LEANAN,
    SM_THAUMATURG, SM_SARUMAN, SM_VORTEX, SM_TIAMAT, SM_KOBOLD, SM_SHELOB,
    SM_LAMPREY, SM_BONNACON, SM_UNGOLIANT, SM_WRAITH, SM_NAZGUL, SM_NONE,
    N_SWORDPOWER, N_FATIGUE,
    MONSTER_EVENT, TREASURE_EVENT, DEATH_EVENT, K_FATIGUE, K_GREED, K_MONSTER,
    ATTACK_MELEE,
    MESSAGE_MORE, MESSAGE_CLEAR
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
    battle["opponent"] = {}
    battle["rounds"] = 0
    battle["speed_spell"] = 0
    battle["strength_spell"] = 0

    opponent = battle["opponent"]
    player["battle"] = battle
    if not "messages" in player.keys():
        player["messages"] = []

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
            # fake opponent type here
            # opponent["type"] = 36


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
        # pick another name
        while (opponent["name"] == "A Mimic"):
            opponent["name"] = monsters[int(roll(0.0, 100.0))]["monster"]["name"]
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
                doCancelMonster(player)
                return
            else:
                battle["introduction"] = "You just subdued %s, thanks to the virgin.\n" % opponent["name"]
                equipment["virgin"] = False
                opponent["energy"] = 0.0
        elif not status["blind"]:
            battle["introduction"] = "You just saw %s running away!\n" % opponent["name"]
            doCancelMonster(player)
            return
        else:
            battle["introduction"] = "You just heard %s running away!\n" % opponent["name"]
            doCancelMonster(player)
            return

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
                broadcast(player, "%s has just defeated %s!\n" % (main["modified_name"], opponent["name"]))

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
                message(player, ["The monster appears to have grown stronger in your absence!\n"])
                opponent["size"] = max(location["circle"], .5 * stats["level"])

        battle["introduction"] = battle["introduction"] + " - (Size: %.0f)\n" % opponent["size"]
        message(player, [battle["introduction"]])

	# allow experimentos to test the speed equation */

    if opponent["special_type"] == SM_MORON:
        if status["type"] == C_EXPER and stats["level"] == 0:
            opponent["speed"] = opponent["max_speed"] = stats["quickness"]
            message(player, ["Recognizing a kindred spirit, A Moron now moves as quickly as you!\n"])
            message(player, ["You feel fully refreshed and healed for battle!\n"])

            doEnergy(player, stats["max_energy"] + equipment["shield"],
                stats["max_energy"], equipment["shield"],
                battle["force_field"], False)
            battle["rounds"] = 0

    # adjust equipment-stealing monsters to knock off unbalanced chars
    if opponent["special_type"] == SM_CERBERUS:
        if (equipment["shield"] / stats["degenerated"] > 100000.0) and stats["degenerated"] < 50:
            opponent["speed"] = stats["max_quickness"] * 4
            opponent["max_speed"] = opponent["speed"]
            message(player, ["Cerberus's eyes flare brightly as he sees the immense amounts of metal you are carrying!\n"])
    elif opponent["special_type"] == SM_JABBERWOCK:
        if (equipment["quicksilver"] / stats["degenerated"] > 500.0) and stats["degenerated"] < 50:
            opponent["speed"] = stats["max_quickness"] * 4
            opponent["max_speed"] = opponent["speed"]
            message(player, ["A Jabberwock whiffles in delight as it sees your immense stash of quicksilver!\n"])
    elif opponent["special_type"] == SM_DARKLORD:
        if equipment["blessing"] and opponent["energy"] > 0 and status["morgoth_count"] == 0:
            message(player, ["Your blessing is consumed by the great evil of your opponent!\n"])
            equipment["blessing"] = False
        elif opponent["energy"] > 0 and status["morgoth_count"] > 0:
            message(player, ["The Dark Lord keeps a safe distance away from you, smelling the scent of its masters blood upon your sword!\n"])

    if equipment["ring_type"] > R_NONE:
        if opponent["special_type"] != SM_IT_COMBAT:
            tt = 1 if opponent["treasure_type"] == 0 else opponent["treasure_type"]
            if random() * 1000 / tt < stats["sin"]:
                message(player, ["You feel compelled to put your ring on your finger!\n"])
                battle["ring_in_use"] = True
                doSin(player, 0.1)
                # TODO: log "%s, %s, forced_ring.\n", lcname, class_name

    if opponent["energy"] > 0:
        doFight(payload, firsthit)
    else:
        # monster dead before we start
        doMonsterKilled(payload)

def doFight(payload, firsthit):
    # loop on monster hit / player hit Check
    # monster might get multiple hits
    # first time into this function the blessing player first hit is made
    # subsequent times in will be from the cient and firsthit will be false

    player = payload["player"]
    main = player["main"]
    equipment = player["equipment"]
    location = player["location"]
    status = player["status"]
    stats = player["stats"]
    battle = player["battle"]
    opponent = battle["opponent"]

    while opponent["energy"] > 0:

        # allow paralyzed monster to wake up
        opponent["speed"] = min(opponent["speed"] + 1.0, opponent["max_speed"])

        # check if blessing gives first hit -- monster has to win
        # initiative extra times depending on sin level --
        # a sinless player always wins first strike

        if firsthit and stats["sin"] > 0:
            monsthit = True
            for i in range (0, floor((stats["sin"] + 1.0) / 1.25)):
                monsthit &= (random() * opponent["speed"]) > (random() * stats["quickness"])

            if monsthit and stats["quickness"] > 0:
                firsthit = False

        # monster is faster
        if (random() * opponent["speed"]) > (random() * stats["quickness"]) \
            and opponent["special_type"] != SM_DARKLORD \
            and opponent["special_type"] != SM_SHRIEKER \
            and opponent["special_type"] != SM_MIMIC \
            and not firsthit:
            # monster gets a hit
            doMonsterHits(payload)
            # check if monster has killed player
            if stats["energy"] <= 0.0 or stats["strength"] <= 0.0:
                # player died
                doPlayerKilled(payload)
                return
        else:
            # player gets a hit
            firsthit = False
            if battle["ring_in_use"]:
                if equipment["ring_type"] != R_DLREG:
                    # age ring
                    equipment["ring_duration"] -= 1
                # regardless of ring type, heal the character
                doEnergy(player, stats["max_energy"] + equipment["shield"],
                    stats["max_energy"], equipment["shield"],
                    battle["force_field"], False)

            # break of the loop so a choice of attack / flee can be made
            break


def doMonsterHits(payload):
    inflict = -1

    player = payload["player"]
    main = player["main"]
    equipment = player["equipment"]
    currency = player["currency"]
    location = player["location"]
    status = player["status"]
    stats = player["stats"]
    battle = player["battle"]
    opponent = battle["opponent"]

    moronmesg = [
        "A Moron queries, 'what do u need to do to b a apprentice? I play for two years'\n",
        "A Moron remembers, 'in the good old days I ruled the realm, I had  a MANs sword'\n",
        "A Moron threatens, 'dont mess with me man, I a l33t haxxor you n00b!'\n",
        "A Moron complains, 'aargh the lag! can u reset the server?'\n",
        "A Moron complains, 'this game needs cheats!'\n",
        "A Moron begs, 'steward can i please have 5k?  ill pay you back.'\n",
        "A Moron complains, 'this game is too hard!'\n",
        "A Moron complains, 'this game is too easy!'\n",
        "A Moron complains, 'this game sucks!'\n",
        "A Moron snarls, 'i hate the changes.  why cant they bring back the old version?'\n",
        "A Moron grumbles, 'wizards never do anything.  why dont they add some pics?'\n",
        "A Moron queries, 'where do i buy stuff?'\n",
        "A Moron whimpers, 'how do I get rid of plague?'\n",
        "A Moron boasts, 'i have a level 8k char, just you wait!'\n",
        "A Moron wonders, 'what do i do with a virgin?\n",
        "A Moron squeals, 'ooh a smurf how cute!\n",
        "A Moron howls, 'but i don't want to read the rules!'\n",
        "A Moron asks, 'how come morons never run out?\n",
        "A Moron snivels, 'why is everything cursed?  this curse rate is too high!'\n",
        "A Moron whines, 'how come a Troll hit me 5 times in a row?  it must be a bug!'\n",
        "A Moron yells, 'HEY ALL COME CHEK OUT MY KNEW GAME!'\n",
        "A Moron slobbers, 'please make me an apprentice please please please'\n",
        "A Moron grouches, 'all the apprentices are power-hungry maniacs'\n",
        "A Moron asserts, 'I'm not a liar, honest!'\n",
        "A Moron sings, 'i love you!  you love me!'\n",
        "A Moron exclaims, 'But I didn't MEAN to kill you!'\n",
        "A Moron curses, 'smurfing smurf smurf!  why can't i swear?'\n",
		"A Moron demands, 'i want a bank to store gold so i can get a bigger shield!'\n",
        "A Moron bawls, 'Waa!  My mommy died!  Hey, will u make me apprentice?'\n",
        "A Moron warns, 'my dad is a wizard, don't mess with me!'\n",
        "A Moron leers, 'hey baby what's your sign?'\n",
        "A Moron drools, 'If I had a pick scroll, I'd pick you!  What's your number?'\n"
    ]

    if stats["quickness"] <= 0:
        # kill a player at speed 0 with no TODO: network - saves time
        # also kill a player at speed 0 once monster inflicts 3 rounds
        # of fatigue so that people won't have to sit forever
        if battle["rounds"] > N_FATIGUE * 3:
            inflict = stats["energy"] + battle["force_field"] + 1.0
            opponent["special_type"] = SM_NONE

    if opponent["special_type"] == SM_DARKLORD:
        # hits just enough to kill player */
        inflict = stats["energy"] + battle["force_field"] + 1.0
    elif opponent["special_type"] == SM_SHRIEKER:

        aNewEvent = newEvent(MONSTER_EVENT, MONSTER_SHRIEKER, 0, 0, "")

        if equipment["shield"] / stats["degenerated"] > 100000.0:
            # Shield too big. Summon a Cerberus
            aNewEvent["arg3"] = 96
        elif equipment["quicksilver"] / stats["degenerated"] > 500.0:
            # Too much quicksilver. Summon a Jabberwock
            aNewEvent["arg3"] = 94
        else:
            # Else summon a large monster
            aNewEvent["arg3"] = roll(70.0, 30.0)
            stackEvent(payload, aNewEvent)
            message(player, ["Shrieeeek!!  You scared it, and it called one of its friends.\n", MESSAGE_MORE, MESSAGE_CLEAR])
            doCancelMonster(player);
            return
    elif opponent["special_type"] == SM_BALROG:
        # if there is no experience to take, do damage
        if (random() > .33 and stats["experience"] > 0 and status["special_type"] < SC_KING):
            # take experience away
            inflict = (.001 + random() * .003) * stats["experience"]
            inflict = min(stats["experience"], inflict)
            # add to strength
            opponent["strength"] += min(.05 * equipment["shield"], floor(sqrt(stats["experience"] / 1800.0)))
            message(player, ["%s lashes his whip and absorbs %.0f experience points from you!\n" % (opponent["name"], inflict)])
            doExperience(player, inflict *- 1, False)
            return
    elif opponent["special_type"] == SM_FAERIES:
        # holy water kills when monster tries to hit
        if equipment["holywater"] >= floor(sqrt(opponent["size"])):
            message(player, ["Your holy water killed it!\n"])
            equipment["holywater"] -= floor(sqrt(opponent["size"]))
            opponent["energy"] = 0.0
            return
    elif opponent["special_type"] == SM_TITAN:
        equipment["shield"] = ceil(equipment["shield"] * .99)
        inflict = floor(1.0 + random() * opponent["strength"])
        inflict = min(inflict, stats["energy"])

        if battle["force_field"] > 0.0:
            # inflict damage through force field
            message(player, ["%s punches through your pitiful force field and hit you for %.0f damage!\n" % (opponent["name"], inflict)])
            battle["force_field"] = 0.0
            doEnergy(player, stats["energy"] - inflict, stats["max_energy"], equipment["shield"], \
                battle["force_field"], False)
            return
        else:
            message(player, ["%s hit you for %.0f damage and damages your shield!\n" % (opponent["name"], inflict)])
    elif opponent["special_type"] == SM_NONE:
        a = "none"
        # normal hit
    elif random() < 0.2 or ( \
        ((opponent["special_type"] == SM_CERBERUS) and \
        (equipment["shield"] / stats["degenerated"] > 50000.0)) or \
        ((opponent["special_type"] == SM_JABBERWOCK) and \
        (equipment["quicksilver"] / stats["degenerated"] > 500.0))):
        # check for magic resistance
        if ((opponent["special_type"] != SM_MODNAR) and \
            (opponent["special_type"] != SM_MORGOTH) and \
            (opponent["special_type"] != SM_MORON) and \
            (opponent["special_type"] != SM_SMURF) and \
            (opponent["special_type"] != SM_IDIOT) and \
            (opponent["special_type"] != SM_MIMIC) and \
            (opponent["special_type"] != SM_SMEAGOL) and \
            (opponent["special_type"] != SM_TROLL) and \
            ((opponent["special_type"] == C_HALFLING) and (random() < 0.25))):
                message(player, ["%s tries to do something special, but you resist the attack!\n" % opponent["name"]])
                return
        if ((opponent["special_type"] != SM_MODNAR) and
            (opponent["special_type"] != SM_MORON) and
            (opponent["special_type"] != SM_SMURF) and
            (opponent["special_type"] != SM_TROLL) and
            (opponent["special_type"] != SM_SMEAGOL) and
            ((opponent["special_type"] != SM_SARUMAN) or
             (equipment["amulets"] >= equipment["charms"])) and
            (opponent["special_type"] != SM_MIMIC)):
                # dwarves/halflings/expers use fewer charms
                dtemp = opponent["treasure_type"] - (floor((status["type"] + 1) * 1.5))
                if dtemp < 1:
                    dtemp = 1
                dtemp2 = ceil(random() * floor(sqrt(opponent["size"]) * dtemp))
                if dtemp2 < dtemp:
                    dtemp2 = dtemp
                if equipment["charms"] >= dtemp2:
                    # TODO: Log "%s, %s, %.0lf charms blocked size %.0lf attack (%.0lf TT %d)\n"
                    message(player, ["%s tries to do something special, but you used %.0lf of your charms to block it!\n" % (opponent["name"], dtemp2)])
                    equipment["charms"] -= dtemp2
                    return
        elif opponent["special_type"] == SM_LEANAN:
            # takes some of the player's strength
            inflict = roll(1.0, opponent["size"] * 4)
            inflict = min(stats["level"], inflict)
            inflict = max(.02 * stats["strength"], inflict)
            if inflict > stats["strength"]:
                message(player, ["%s sucks all of your strength away, destroying your soul!\n" % opponent["name"]])
                inflict = stats["strength"]
            else:
                message(player, ["%s sapped %0.f of your strength!\n" % (opponent["name"], inflict)])
            doStrength(player, stats["max_strength"] - inflict, equipment["sword"], battle["strength_spell"], False)
            return
        elif opponent["special_type"] == SM_THAUMATURG:
            # transport player */
            message(player, ["%s transported you!\n" % opponent["name"]])
            aNewEvent = newEvent(MOVE_EVENT, 0, 0, A_FAR, "")
            doCancelMonster(player)
            return
        elif opponent["special_type"] == SM_SARUMAN:
            if equipment["charms"] > equipment["amulets"]:
                message(player, ["%s turns your charms into amulets and vice versa!\n" % opponent["name"]])
                dtemp = equipment["charms"]
                equipment["charms"] = equipment["amulets"]
                equipment["amulets"] = dtemp
            elif equipment["palantir"]:
                # take away palantir
                message(player, ["Wormtongue stole your palantir!\n"])
                doPalantir(player, False, False);
            elif random() > 0.5:
                # gems turn to gold
                message(player, ["%s transformed your gems into gold!\n" % opponent["name"]])
                doGold(player, currency["gems"], False)
                doGems(c, currency["gems"], False)
            else:
                # scramble some stats
                message(player, ["%s casts a spell and you feel different!\n" % opponent["name"]])
                doScrambleStats(player)
            return
        elif opponent["special_type"] == SM_VORTEX:
            # suck up some mana
            inflict = roll(0, 50 * opponent["size"])
            inflict = min(stats["mana"], floor(inflict))
            message(player, ["%s sucked up %.0f of your mana!\n" % (opponent["name"], inflict)])
            doMana(player, -inflict, False)
            return
        elif opponent["special_type"] == SM_SUCCUBUS:
            # take some brains
            message(player, ["%s caresses you and whispers sweet nothings in your ear.  You feel foolish!\n" % opponent["name"]])
            stats["brains"] *= 0.8
            return
        elif opponent["special_type"] == SM_TIAMAT:
            # take some gold and gems
            message(player, ["%s took half your gold and gems and flew off.\n" % opponent["name"]])
            doGold(player, -floor(currency["gold"] / 2.0), False)
            doGems(player, -floor(currency["gems"] / 2.0), False)
            doCancelMonster(player)
            return
        elif opponent["special_type"] == SM_KOBOLD:
            # steal a gold piece and run
            if currency["gold"] > 0:
                message(player, ["%s stole one gold piece and ran away.\n" % opponent["name"]])
                doGold(c, -1.0, False);
                doCancelMonster(player)
                return
        elif opponent["special_type"] == SM_SHELOB:
            # bite and (medium) poison
            message(player, ["%s has bitten and poisoned you!\n" % opponent["name"]])
            doAdjustedPoison(player, 1.0)
            return
        elif opponent["special_type"] == SM_LAMPREY:
            if (random() * 10 < (opponent["size"] / 2) - 1):
                # bite and (small) poison
                message(player, ["%s bit and poisoned you!\n" % opponent["name"]])
                doAdjustedPoison(player, 0.25)
            return
        elif opponent["special_type"] == SM_BONNACON:
            # fart and run
            message(player, ["%s farted and scampered off.\n" % opponent["name"]])
            # damage from fumes
            doEnergy(player, stats["energy"] / 2.0, stats["max_energy"], equipment["shield"], battle["force_field"], False)
            doCancelMonster(player)
            return
        elif opponent["special_type"] == SM_SMEAGOL:
            if equipment["ring_type"] != R_NONE:
                # try to steal ring
                if random() > 0.1:
                    message(player, ["%s tried to steal your ring, but was unsuccessful.\n" % opponent["name"]])
                else:
                    message(player, ["%s tried to steal your ring and ran away with it!\n" % opponent["name"]])
                    doRing(player, R_NONE, False)
                    doCancelMonster(player)
                return
            elif status["type"] == C_HALFLING:
                if stats["sin"] > 2.0:
                    message(player, ["%s cries, 'Thief!  Baggins!  We hates it, we hates it, for ever and ever!'\n" % opponent["name"]])
                else:
                    message(player, ["%s wonders, 'What has it got in itsss pocketsss?'\n" % opponent["name"]])
        elif opponent["special_type"] == SM_CERBERUS:
            # take all metal treasures
            message(player, ["%s took all your metal treasures and ran off!\n" % opponent["name"]])

            # TODO: sprintf(string_buffer, "%s, %s, cerbed.\n",
            # Do_log(COMBAT_LOG, &string_buffer);

            doEnergy(player, stats["energy"], stats["max_energy"], 0.0, battle["force_field"], False)
            doStrength(player, stats["max_strength"], 0.0, battle["strength_spell"], False)
            if stats["level"] > MIN_KING:
                doCrowns(player, -equipment["crowns"], False)
            doGold(c, -currency["gold"], False);
            doCancelMonster(player)
            return
        elif opponent["special_type"] == SM_UNGOLIANT:
            # (large) poison and take a quickness
            message(player, ["%s stung you with a virulent poison.  You begin to slow down!\n" % opponent["name"]])
            doAdjustedPoison(player, 5.0);
            doSpeed(player, stats["max_quickness"] - 1.0, equipment["quicksilver"], battle["speed_spell"], False)
            return
        elif opponent["special_type"] == SM_JABBERWOCK:
            if random() > .75 or equipment["quicksilver"] == 0:
                # fly away, and leave either a Jubjub bird or Bandersnatch
                message(player, ["%s flew away, and left you to contend with one of its friends.\n" % opponent["name"]])
                aNewEvent = newEvent(MONSTER_EVENT, MONSTER_JABBERWOCK, 0, 0, "")
                if random.choice([True, False]):
                    # Jubjub Bird
                    aNewEvent["arg3"] = 55
                else:
                    # Bandersnatch
                    aNewEvent["arg3"] = 71
                # TODO: Deal with monster event
                doCancelMonster(player)
                return
            else:
                # burble, causing the player to lose quicksilver
                message(player, ["%s burbles as it drinks half of your quicksilver!\n" % opponent["name"]])
                doSpeed(player, stats["max_quickness"], floor(equipment["quicksilver"] * .5), battle["speed_spell"], False)
                return
        elif opponent["special_type"] == SM_TROLL:
            # partially regenerate monster
            message(player, ["%s partially regenerated his energy!\n" % opponent["name"]])
            opponent["energy"] += floor((opponent["max_energy"] - opponent["energy"]) / 2.0)
            opponent["strength"] = opponent["max_strength"]
            opponent["speed"] = opponent["max_speed"]
            battle["melee_damage"] = battle["skirmish_damage"] = 0.0
            return
        elif opponent["special_type"] == SM_WRAITH:
            if not status["blind"]:
                # make blind
                message(player, ["%s blinded you!\n" % opponent["name"]])
                status["blind"] = True
                opponent["name"] = "A monster"
            return
        elif opponent["special_type"] == SM_IDIOT:
            message(player, ["%s drools.\n" % opponent["name"]])
        elif opponent["special_type"] == SM_MORON:
            # don't subject males to pickup line */
            if stats["gender"] == "Female":
                msg = moronmesg[int(roll(0.0, len(moronmesg)))]
            else:
                msg = moronmesg[int(roll(0.0, len(moronmesg)-2))]
            message(player, [msg])
        elif opponent["special_type"] == SM_SMURF:

            if random() < .5:
                if random() < .5:
                    if stats["gender"] == "Female":
                        message(player, ["%s sneers, 'Smurfette is prettier than you!'\n" % opponent["name"]])
                    elif status["type"] == C_MAGIC:
                        message(player, ["%s yells out, 'Aah!  I'm being attacked by Gargamel!'\n" % opponent["name"]])
                    elif status["type"] == C_HALFLING:
                        message(player, ["%s wonders, 'Are you Angry Smurf?'\n" % opponent["name"]])
                    elif status["type"] == C_DWARF:
                        message(player, ["%s howls, 'A giant!  Run!'\n" % opponent["name"]])
                    else:
                        message(player, ["%s snarls, 'Smurf you, you smurfing smurf!'\n" % opponent["name"]])
                else:
                    message(player, ["%s shrieks, 'Help, Papa Smurf, Help!'\n" % opponent["name"]])
            else:
                message(player, ["%s sings, 'Lah lah la lah la la!'\n" % opponent["name"]])
        elif opponent["special_type"] == SM_NAZGUL:
            # try to take ring if player has one
            if equipment["ring_type"] != R_NONE:
                # player has a ring
                message(player, ["%s demands your ring.  Do you hand it over?\n" % opponent["name"]])

                #TODO
                #if (Do_yes_no(c, &theAnswer) == S_NORM && theAnswer == 0) {

                theAnswer = random.choice(["Yes", "No"])
                if theAnswer == "Yes":
                    # take ring away
                    doRing(player, R_NONE, False)
                    battle["ring_in_use"] = False
                    doCancelMonster(battle["player"])
                    return
                else:
                    opponent["strength"] *= 1.1 + .4 * random()
                    opponent["max_speed"] += 1
                    opponent["speed"] = opponent["speed"] + ceil((opponent["max_speed"] - opponent["speed"]) / 2)
                    message(player, ["Angered by your refusal, %s attacks harder and faster!.\n" % opponent["name"]])

            # also fall through to the curse
            # curse the player

            if equipment["blessing"] == True:
                message(player, ["%s hurls an eldritch curse at you!  But you were saved by your blessing!\n" % opponent["name"]])
                doBlessing(player, False, False);
            else:
                message(player, ["%s hurls an eldritch curse at you!  You feel weak and ill!\n" % opponent["name"]])


            doEnergy(player, (stats["energy"] + battle["force_field"]) / 2, \
                stats["max_energy"] * .99, equipment["shield"], \
                battle["force_field"], False)

            doAdjustedPoison(player, 0.5)
            return

    # fall through to here if monster inflicts a normal hit
    if inflict == -1:
        inflict = floor(1.0 + random() * opponent["strength"])
    message(player, ["%s hit you for %.0f damage!\n" % (opponent["name"], inflict)])
    if battle["force_field"] < inflict:
        doEnergy(player, stats["energy"] + battle["force_field"] - inflict, \
            stats["max_energy"], equipment["shield"], 0, False)
    else:
        doEnergy(player, stats["energy"], stats["max_energy"], equipment["shield"], \
            battle["force_field"] - inflict, False)
    return

def doPlayerHits(payload):

    player = payload["player"]
    action = payload["action"]
    main = player["main"]
    equipment = player["equipment"]
    currency = player["currency"]
    location = player["location"]
    status = player["status"]
    stats = player["stats"]
    battle = player["battle"]
    opponent = battle["opponent"]

    if action["arg1"] == ATTACK_MELEE:
        might = stats["strength"] * (1 + sqrt(equipment["sword"]) * N_SWORDPOWER) + battle["strength_spell"]

        if battle["ring_in_use"]:
            might *= 2

        inflict = floor((.5 + 1.3 * random()) * might);

        battle["melee_damage"] += inflict

        opponent["strength"] = opponent["max_strength"] - \
            (battle["melee_damage"] / opponent["max_energy"]) * \
            (opponent["max_strength"] / 3.0)

        doHitMonster(payload, inflict)

        # give the character fatigue
        battle["rounds"] += 1
        doSpeed(player, stats["max_quickness"], equipment["quicksilver"], battle["speed_spell"], False)

    # Does the monster get a hit back?!
    if "opponent" in battle.keys():
        doFight(payload, False)

def doHitMonster(payload, inflict):

    player = payload["player"]
    main = player["main"]
    equipment = player["equipment"]
    currency = player["currency"]
    location = player["location"]
    status = player["status"]
    stats = player["stats"]
    battle = player["battle"]
    opponent = battle["opponent"]
    battle["messages"] = []

    message(player, ["You hit %s for %.0f damage!\n" % (opponent["name"], inflict)])
    opponent["shield"] -= inflict

    if opponent["shield"] < 0.0:
        opponent["energy"] += opponent["shield"]
        opponent["shield"] = 0.0

    if opponent["special_type"] != SM_IT_COMBAT:
        if opponent["energy"] > 0.0:
            if opponent["special_type"] == SM_DARKLORD or opponent["special_type"] == SM_SHRIEKER:
                # special monster didn't die
                doMonsterHits(payload)
        else:

            # monster died.  print message.
            if opponent["special_type"] == SM_DARKLORD:
                broadcast(player, "%s has just defeated the Dark Lord!\n" % main["modified_name"])
            elif opponent["special_type"] == SM_MORGOTH:
                message(player, ["You have overthrown Morgoth!  But beware, he will return...\n", MESSAGE_MORE, MESSAGE_CLEAR])
                status["morgoth_count"] = 500
                broadcast(player, "All hail %s for overthrowing Morgoth, Enemy of the Vala!\n" % main["modified_name"])
            elif opponent["special_type"] == SM_SMURF and not status["blind"]:
                message(player, ["You finally manage to squish the Smurf.  Good work, %s.\n" % main["modified_name"], MESSAGE_MORE, MESSAGE_CLEAR])
            else:
                # all other types of monsters
                message(player, ["You killed it.  Good work, %s.\n" % main["modified_name"], MESSAGE_MORE, MESSAGE_CLEAR])

            if opponent["special_type"] == SM_MIMIC and opponent["name"] != "A Mimic" and not status["blind"]:
                message(player, ["%s's body slowly changes into the form of a mimic.\n" % opponent["name"], MESSAGE_MORE, MESSAGE_CLEAR])

            doMonsterKilled(payload)

def doCancelMonster(player):
    print("doCancelMonster")
    print(player["battle"]["opponent"])
    print(player["messages"])
    #del player["battle"]["opponent"]

def doMonsterKilled(payload):

    player = payload["player"]
    main = player["main"]
    equipment = player["equipment"]
    currency = player["currency"]
    location = player["location"]
    status = player["status"]
    stats = player["stats"]
    battle = player["battle"]
    opponent = battle["opponent"]

    if opponent["experience"]:
        doExperience(player, opponent["experience"], False)

    # TODO: log the victory
    # sprintf(string_buffer, "%s killed size %.0lf %s\n", c->player.lcname, c->battle.opponent->size, c->battle.opponent->realName);
	# Do_log(BATTLE_LOG, &string_buffer);

    # monster flocks */
    if random() < opponent["flock_percent"] / 100.0:
        aNewEvent = newEvent(MONSTER_EVENT, MONSTER_FLOCKED, opponent["size"], opponent["type"], 0, "")
    else:
        # last fight in sequence, remove timeout penalty
        battle["timeouts"] = 0

    # monster has treasure
    if (opponent["treasure_type"] > 0.0 and (random() > 0.2 + pow(0.4, opponent["size"] / 3.0))) or \
        opponent["special_type"] == SM_UNICORN:
        aNewEvent = newEvent(TREASURE_EVENT, opponent["size"], 0, 0, "")
        # unicorns will always drop trove or pick scrolls */
        if opponent["special_type"] == SM_UNICORN:
            if stats["level"] <= 100 - currency["gems"]:
                aNewEvent["arg2"] = 1
            else:
                aNewEvent["arg2"] = 5
        aNewEvent["arg3"] = opponent["treasure_type"]
        stackEvent(payload, aNewEvent)

    if equipment["ring_duration"] <= 0:
    	if equipment["ring_type"] == R_NAZREG:
    	    doRing(player, R_NONE, False);
    	    message(player, [MESSAGE_CLEAR, "Your ring vanishes!\n", MESSAGE_MORE])
    	elif equipment["ring_type"] == R_BAD:
    	    doRing(player, R_SPOILED, False)
    	elif equipment["ring_type"] == R_SPOILED:
            aNewEvent = newEvent(DEATH_EVENT, 0, 0, K_RING)
            doPlayerKilled(payload)

	# remove player bonuses */
    doEnergy(player, stats["energy"], stats["max_energy"], equipment["shield"], 0, False)
    doStrength(player, stats["max_strength"], equipment["sword"], 0, False)
    doSpeed(player, stats["max_quickness"], equipment["quicksilver"], 0, False)

    battle["force_field"] = 0
    battle["strength_spell"] = 0
    battle["speed_spell"] = 0

    #del player["battle"]["opponent"]

def doPlayerKilled(payload):

    player = payload["player"]
    main = player["main"]
    equipment = player["equipment"]
    currency = player["currency"]
    location = player["location"]
    status = player["status"]
    stats = player["stats"]
    battle = player["battle"]
    opponent = battle["opponent"]

    deathEvent = newEvent(DEATH_EVENT, battle["ring_in_use"], 0, 0, "")
    # check if player died from greed or fatigue
    if stats["quickness"] == 0:
        if battle["rounds"] >= stats["max_quickness"] * N_FATIGUE:
            deathEvent["arg3"] = K_FATIGUE
        else:
            deathEvent["arg3"] = K_GREED
    else:
        deathEvent["arg3"] = K_MONSTER
    deathEvent["arg4"] = opponent["real_name"]
    doCancelMonster(player)
    # TODO: Log the battle loss
    handleEvent()
    message(player, ["Your die a horrible death!\n", MESSAGE_MORE, MESSAGE_CLEAR])
