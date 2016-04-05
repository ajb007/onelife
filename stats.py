from math import floor
from constants import R_DLREG, DEATH_EVENT, K_SIN
from event import newEvent
from random import random

def doEnergy(player, energy, maxEnergy, shield, forceShield, force):

    player["knight_energy"] = 0.0 # Move to client.py
    player["knight_quickness"] = 0.0 # Move to client.py
    player["force_field"] = 0.0 # Move to battle.py

    stats = player["stats"]
    equipment = player["equipment"]

    maxEnergy = floor(maxEnergy)
    shield = floor(shield)
    energy = floor(energy)
    forceShield = floor(forceShield)

    if maxEnergy < 0:
	    maxEnergy = 0

    if energy > maxEnergy + shield + player["knight_energy"]:
        energy = maxEnergy + shield + player["knight_energy"]

	# check for changes
    if stats["energy"] != energy or stats["max_energy"] != maxEnergy or equipment["shield"] != shield or player["force_field"] != forceShield or force:
	    stats["energy"] = energy
	    stats["max_energy"] = maxEnergy
	    player["force_field"] = forceShield

    if equipment["shield"] != shield or force:
        equipment["shield"] = shield

def doSin(player, sin):

    messages = []
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
        messages.append("Your blessing is consumed by the evil of your actions!\n")
        equipment["blessing"] = False

    if stats["sin"] > 25.0 + random() * 25.0:
        event = newEvent(DEATH_EVENT, 0, 0, K_SIN, "")
    else:
        messages.append("You cackle gleefully at the chaos you are causing!\n")

    return messages, event
