"""Jackknifed truck in heavy rain realistic stress case."""

from storm_skin import *
from freight_cast import *
from hydroplane_watch import *

model scenic.simulators.newtonian.model

param severity = 3
param reaction_window = 2

require True
terminate after 60 steps
record initial 1 as 'JackknifeRain_start'
record final 2 as 'JackknifeRain_end'

scenario Main():
    precondition: True
    invariant: True
    setup:
        ego = new Object
        support = new Object
        mutate ego, support
    compose:
        do JackknifeRainEnvironment()
        do JackknifeRainTraffic()
