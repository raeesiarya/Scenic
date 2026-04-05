"""Black ice on curved off-ramp realistic stress case."""

from frost_curve import *
from ramp_convoy import *
from yaw_watch import *

model scenic.simulators.newtonian.model

param severity = 3
param reaction_window = 2

require True
terminate after 60 steps
record initial 1 as 'BlackIceRamp_start'
record final 2 as 'BlackIceRamp_end'

scenario Main():
    precondition: True
    invariant: True
    setup:
        ego = new Object
        support = new Object
        mutate ego, support
    compose:
        do BlackIceRampEnvironment()
        do BlackIceRampTraffic()
