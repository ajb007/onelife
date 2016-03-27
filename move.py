from math import floor, cos, sin
from flask import jsonify
import macros
from random import random

def moveClose(x, y, maxDistance):

    angle = 0.0
    distance = 0.0
    angle = random() * 2 * 3.14159
    distance = random() * maxDistance
    if (distance < 1.0):
	    distance = 1.0

    c = floor(cos(angle) * distance + .5)
    s = floor(sin(angle) * distance + .5)

	# add half a point because floor(-3.25) = -4 */
    x += floor(cos(angle) * distance + .5)
    y += floor(sin(angle) * distance + .5)

    return {"x":x,"y":y}
