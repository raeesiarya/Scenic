"""Highway debris cascade realistic stress case."""

from cargo_corridor import *
from freeway_pack import *
from clearance_watch import *

model scenic.simulators.newtonian.model

param severity = 3
param reaction_window = 2

require True
terminate after 60 steps
record initial 1 as 'DebrisCascade_start'
record final 2 as 'DebrisCascade_end'

scenario Main():
    precondition: True
    invariant: True
    setup:
        ego = new Object
        support = new Object
        mutate ego, support
    compose:
        do DebrisCascadeEnvironment()
        do DebrisCascadeTraffic()
