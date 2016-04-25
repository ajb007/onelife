import json
from math import floor, sqrt, pow, fabs
from event import newEvent
from random import random
from macros import calcLevel, roll, sgn, any
from messages import message, broadcast
from constants import (
    R_DLREG, DEATH_EVENT, K_SIN, N_FATIGUE, C_EXPER, C_DWARF,
    MAX_STEWARD, MAX_KING, SC_NONE, SC_KING, SC_STEWARD, SC_COUNCIL, SC_KNIGHT,
    R_NONE, R_NAZREG, R_DLREG, R_BAD, R_SPOILED,
    MESSAGE_MORE, MESSAGE_CLEAR
)

playerTypes = ""
playerType = ""

def initPlayerTypes():
    global playerType
    global playerTypes
    with open("data/playerTypes.json") as data_file:
        data = json.load(data_file)
    playerTypes = data["playerTypes"]

def getPlayerType(type):
    global playerType
    global playerTypes
    for playerType in playerTypes:
        if playerType["type"] == type:
            return playerType

def doEnergy(player, energy, maxEnergy, shield, forceShield, force):

    stats = player["stats"]
    status = player["status"]
    equipment = player["equipment"]
    knight = player["knight"]

    maxEnergy = floor(maxEnergy)
    shield = floor(shield)
    energy = floor(energy)
    forceShield = floor(forceShield)

    if maxEnergy < 0:
	    maxEnergy = 0

    if energy > maxEnergy + shield + knight["knight_energy"]:
        energy = maxEnergy + shield + knight["knight_energy"]

	# check for changes
    if stats["energy"] != energy or stats["max_energy"] != maxEnergy or equipment["shield"] != shield or status["force_field"] != forceShield or force:
	    stats["energy"] = energy
	    stats["max_energy"] = maxEnergy
	    status["force_field"] = forceShield

    if equipment["shield"] != shield or force:
        equipment["shield"] = shield

def doSin(player, sin):

    event = {}

    stats = player["stats"]
    status = player["status"]
    equipment = player["equipment"]

    if equipment["ring_type"] == R_DLREG:
        stats["sin"] += sin * 2
    else:
        stats["sin"] += sin

    if stats["sin"] < 0.0:
        stats["sin"] = 0.0

    if equipment["blessing"] and stats["sin"] > ((1500.0 + stats["level"]) / (stats["level"] + 30)):
        message(player, ["Your blessing is consumed by the evil of your actions!\n", MESSAGE_MORE, MESSAGE_CLEAR])
        equipment["blessing"] = False

    if stats["sin"] > 25.0 + random() * 25.0:
        aNewEvent = newEvent(DEATH_EVENT, 0, 0, K_SIN, "")
        # TODO: File event
    elif stats["sin"] > 20.0 and random() < .2:
        message(player, ["You cackle gleefully at the chaos you are causing!\n", MESSAGE_MORE, MESSAGE_CLEAR])

def doSpeed(player, maxQuickness, quicksilver, speedSpell, force):

    stats = player["stats"]
    status = player["status"]
    equipment = player["equipment"]
    currency = player["currency"]
    knight = player["knight"]

    rounds = 0
    speed_spell = 0.0

    if "battle" in player.keys():
        rounds = player["battle"]["rounds"]
        speed_spell = player["battle"]["speed_spell"]

    dtemp = 0.0
    quickness = 0

    # player can have a minimum of 0 quickness
    if maxQuickness < 0.0:
        maxQuickness = 0.0

	#see if the player is carrying too much treasure */
    if status["wizard"] < 3:
        ptype = getPlayerType(status["type"])["stats"][0]
        dtemp = ((currency["gold"] + currency["gems"] / 2.0) - 1000.0) / ptype["gold_tote"] - stats["level"]
    else:
        dtemp = 0.0

    # gold can only slow a player down */
    if dtemp < 0.0:
        dtemp = 0.0

	# subtract speed for excessive combat
    dtemp += rounds / N_FATIGUE

    quickness = maxQuickness + sqrt(floor(quicksilver)) + speedSpell + knight["knight_quickness"] - dtemp

    if quickness < 0.0:
        quickness = 0.0

    if stats["quickness"] != quickness or stats["max_quickness"] != maxQuickness or \
        equipment["quicksilver"] != quicksilver or speed_spell != speedSpell or force:

        stats["quickness"] = quickness
        stats["max_quickness"] = maxQuickness
        speed_spell = speedSpell

        if equipment["quicksilver"] != quicksilver or force:
            equipment["quicksilver"] = quicksilver

def doExperience(player, experience, force):

    stats = player["stats"]
    status = player["status"]
    battle = player["battle"]
    knight = player["knight"]
    equipment = player["equipment"]

    force_field = 0.0
    strength_spell = 0.0
    if "battle" in player.keys():
        force_field = player["battle"]["force_field"]
        strength_spell = player["battle"]["strength_spell"]

    # add the experience
    stats["experience"] += experience
    # determine the new level
    newLevel = calcLevel(stats["experience"])
    inc = newLevel - stats["level"]
    # if we've gone up any levels
    if inc > 0:
        # make sure we send the level information
        force = True
        stats["level"] = newLevel
        if status["type"] == C_EXPER:
            # roll a type to use for increment */
            ptype = getPlayerType(int(roll(C_MAGIC, (C_HALFLING-C_MAGIC + 1))))["stats"][0]
        else:
            ptype = getPlayerType(status["type"])["stats"][0]

        doEnergy(player, stats["energy"] + ptype["energy"]["increase"] * inc,
            stats["max_energy"] + ptype["energy"]["increase"] * inc,
            equipment["shield"], force_field, False)

        doStrength(player, stats["max_strength"] + ptype["strength"]["increase"] * inc,
            equipment["sword"], strength_spell, False)

        doMana(player, ptype["mana"]["increase"] * inc, False)

        stats["brains"] += ptype["brains"]["increase"] * inc
        stats["magic_level"] = stats["magic_level"] + ptype["magic_level"]["increase"] * inc

        if (status["special_type"] == SC_KNIGHT):
            # knights may get more energy
            doEnergy(player, stats["energy"] - knight["knight_energy"] +
                floor(stats["max_energy"] / 4), stats["max_energy"],
                equipment["shield"], force_field, False)
            knight["knight_energy"] = floor(stats["max_energy"] / 4)

        if stats["level"] == 1000.0:
            # send congratulations message
            message(player, ["Congratulations on reaching level 1000!  The throne awaits...\n", MESSAGE_MORE, MESSAGE_CLEAR])

        if stats["level"] >= MAX_STEWARD and status["special_type"] == SC_STEWARD:
		    # no longer able to be steward -- dethrone
	        message(player, ["After level 200, you can no longer be steward.\n"])
            # Do_dethrone(c);

        if stats["level"] >= MAX_KING and status["special_type"] == SC_KING:
		    # no longer able to be king -- dethrone */
            message(player, ["After level 2000, you can no longer be king or queen.\n"])
            # Do_dethrone(c);
            status["special_type"] = SC_NONE

            if equipment["crowns"] > 0:
                message(player, ["Your crowns were cashed in.\n", MESSAGE_MORE, MESSAGE_CLEAR])
                doGold(player, equipment["crowns"] * 5000.0, False)
                doCrowns(player, equipment["crowns"] * -1, False)

                #if status["special_type"] == SC_KING:
    		        #TODO: Do_dethrone(c);

        elif stats["level"] >= MAX_STEWARD and stats["level"] < 1000.0:

            message(player, ["Your staves were cashed in.\n", MESSAGE_MORE, MESSAGE_CLEAR])

            doGold(player, equipment["crowns"] * 1000.0, False)
            doCrowns(player, equipment["crowns"] * -1, False)

            #if status["special_type"]== SC_STEWARD:
		        #TODO: Do_dethrone(c);

        if stats["level"] >= 3000.0 and status["special_type"] < SC_COUNCIL:

	        # if by some chance this person is king or knight, dethrone him */
            #if status["special_type"] == SC_KING or status["special_type"] == SC_KNIGHT:
        		#TODO: Do_dethrone(c);

            broadcast("The Council of the Wise announces its newest member, %s.\n" % player["main"]["name"])

             # TODO: Implement rest of doExperience

def doStrength(player, maxStrength, sword, strengthSpell, force):

    stats = player["stats"]
    status = player["status"]
    equipment = player["equipment"]

    strength_spell = 0.0
    if "battle" in player.keys():
        strength_spell = player["battle"]["strength_spell"]

    ptype = getPlayerType(status["type"])["stats"][0]

    # player can have a minimum of 0 strength */
    if maxStrength < 0:
        maxStrength = 0

    #alculate strength based on poison */
    strength = 1.0 - stats["poison"] * ptype["weakness"] / 800.0

    if strength > 1.0:
    	strength = 1.0

    if strength < .1:
    	strength = .1

    strength = maxStrength * strength

	# check for changes
    if stats["strength"] != strength or stats["max_strength"] != maxStrength or \
        equipment["sword"] != sword or strength_spell != strengthSpell or \
        force:

        stats["strength"] = strength;
        stats["max_strength"] = maxStrength;
        if "battle" in player.keys():
            player["battle"]["strength_spell"] = strengthSpell

        if equipment["sword"] != sword or force:
            equipment["sword"] = sword

def doMana(player, mana, force):
    # make sure we're still under the maximum mana
    stats = player["stats"]
    status = player["status"]
    ptype = getPlayerType(status["type"])["stats"][0]

    newMana = floor(stats["mana"] + mana)

    maxMana = 1000.0 + stats["level"] * ptype["max_mana"]

    if newMana > maxMana:
        newMana = maxMana

    if newMana != stats["mana"] or force:
        stats["mana"] = newMana

def doGold(player, gold, force):

    currency = player["currency"]
    stats = player["stats"]
    equipment = player["equipment"]
    speed_spell = 0.0
    if "battle" in player.keys():
        speed_spell = player["battle"]["speed_spell"]

    if gold != 0:
        force = True

    if currency["gold"] + gold > 0:
        currency["gold"] = floor(currency["gold"] + gold)
    else:
        currency["gold"] = 0

    doSpeed(player, stats["max_quickness"], equipment["quicksilver"], speed_spell, False)

def doGems(player, gems, force):

    currency = player["currency"]
    stats = player["stats"]
    equipment = player["equipment"]
    speed_spell = 0.0
    if "battle" in player.keys():
        speed_spell = player["battle"]["speed_spell"]

    if gems != 0:
        force = True

    if currency["gems"] + gems > 0:
        currency["gems"] = floor(currency["gems"] + gems)
    else:
        currency["gems"] = 0

    doSpeed(player, stats["max_quickness"], equipment["quicksilver"], speed_spell, False)

def doCrowns(player, crowns, force):

    equipment = player["equipment"]
    crownFlag = any(equipment["crowns"])

    if crowns != 0:
        equipment["crowns"] = equipment["crowns"] + crowns
        if equipment["crowns"] < 0:
            equipment["crowns"] = 0.0

    if crownFlag != any(equipment["crowns"]):

        crownFlag = not crownFlag
        force = True
        #Do_player_description(c);

def doPalantir(player,  palantir, force):

    equipment = player["equipment"]

    if palantir != equipment["palantir"] or force:
        equipment["palantir"] = palantir

    # if no palantir, kick player out of the palantir channel
    # TODO:
    """
    if ((c->player.palantir == FALSE) &&
    (c->channel == 8)) {

    c->channel = 1;

    c->game->hearAllChannels = HEAR_SELF;

    Do_lock_mutex(&c->realm->realm_lock);
    Do_player_description(c);
    Do_unlock_mutex(&c->realm->realm_lock);

    Do_send_specification(c, CHANGE_PLAYER_EVENT);
    """

def doScrambleStats(player):
    #TODO
    print("doScrambleStats")

def doAdjustedPoison(player, poison):

    location = player["location"]

    dtemp = location["circle"] - 17
    poison *= (sgn(dtemp) * pow(fabs(dtemp), .33) + 5.52) / 3
    doPoison(player, poison)

def doPoison(player, poison):

    stats = player["stats"]
    equipment = player["equipment"]
    strength_spell = 0.0
    if "battle" in player.keys():
        strength_spell = player["battle"]["strength_spell"]

    if poison != 0:
        stats["poison"] += poison

    if stats["poison"] < 1e-4:
        stats["poison"] = 0.0

    doStrength(player, stats["max_strength"], equipment["sword"], strength_spell, False)

def doRing(player, ring, force):

    equipment = player["equipment"]
    status = player["status"]

    if ring == R_NONE:

        if equipment["ring_type"] != R_NONE:
            equipment["ring_type"] = R_NONE

    elif ring == R_NAZREG:

        if equipment["ring_type"] == R_NONE:
            equipment["ring_type"] = R_NAZREG
            equipment["ring_duration"] = random() * random() * 150 + 1

    elif ring == R_DLREG:

        if equipment["ring_type"] == R_NONE:
            equipment["ring_type"] = R_DLREG
            equipment["ring_duration"] = 0

    elif ring == R_BAD:

        if equipment["ring_type"] == R_NONE:
            equipment["ring_type"] = R_BAD;
            ptype = getPlayerType(status["type"])["stats"][0]
            equipment["ring_duration"] = 15 + ptype["ring_duration"] + int(roll(0,5))

    elif ring == R_SPOILED:

        if equipment["ring_type"] == R_BAD:
            equipment["ring_type"] = R_SPOILED
            equipment["ring_duration"] = roll(10.0, 25.0)

def doBlessing(player, blessing, force):
    player["equipment"]["blessing"] = blessing

def doRest(player):

    status = player["status"]
    stats = player["stats"]
    location = player["location"]
    equipment = player["equipment"]

    force_field = 0.0
    speed_spell = 0.0

    if "battle" in player.keys():
        force_field = player["battle"]["force_field"]
        speed_spell = player["battle"]["speed_spell"]

    if status["type"] == C_DWARF:
        doEnergy(player, stats["energy"] + (stats["max_energy"] + equipment["shield"]) / 12.0 + stats["level"] / 3.0 + 2.0,
            stats["max_energy"],
            equipment["shield"],
            force_field, False)
    else:
        doEnergy(player, stats["energy"] + (stats["max_energy"] + equipment["shield"]) / 15.0 + stats["level"] / 3.0 + 2.0,
            stats["max_energy"],
            equipment["shield"],
            force_field, False)

    # cannot find mana if cloaked
    if not status["cloaked"]:
        addMana = floor((location["circle"] + stats["level"]) / 5.0)
        if addMana < 1.0:
            addMana = 1.0
        doMana(player, addMana, False);

    # remove combat fatigue
    if "battle" in player.keys():
        battle = player["battle"]
        if battle["rounds"] > 0:
            battle["rounds"] -= 30
        if battle["rounds"] < 0:
            battle["rounds"] = 0

    doSpeed(player, stats["max_quickness"], equipment["quicksilver"], speed_spell, False)
