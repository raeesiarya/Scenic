"""Broken traffic lights at four-way intersection realistic stress case."""

from junction_canvas import *
from approach_cast import *
from rightofway_watch import *

model scenic.simulators.newtonian.model

param severity = 3
param reaction_window = 2

require True
terminate after 60 steps
record initial 1 as 'BrokenLights_start'
record final 2 as 'BrokenLights_end'

scenario Main():
    precondition: True
    invariant: True
    setup:
        ego = new Object
        support = new Object
        mutate ego, support
    compose:
        do BrokenLightsEnvironment()
        do BrokenLightsTraffic()
