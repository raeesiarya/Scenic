"""Multi-car pileup in fog realistic stress case."""

from weather_blanket import *
from convoy_orbits import *
from visibility_alarm import *

model scenic.simulators.newtonian.model

param severity = 3
param reaction_window = 2

require True
terminate after 60 steps
record initial 1 as 'PileupFog_start'
record final 2 as 'PileupFog_end'

scenario Main():
    precondition: True
    invariant: True
    setup:
        ego = new Object
        support = new Object
        mutate ego, support
    compose:
        do PileupFogEnvironment()
        do PileupFogTraffic()
