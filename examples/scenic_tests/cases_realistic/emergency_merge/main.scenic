"""Emergency vehicle during lane merge realistic stress case."""

from merge_surface import *
from lane_cast import *
from gap_alarm import *

model scenic.simulators.newtonian.model

param severity = 3
param reaction_window = 2

require True
terminate after 60 steps
record initial 1 as 'EmergencyMerge_start'
record final 2 as 'EmergencyMerge_end'

scenario Main():
    precondition: True
    invariant: True
    setup:
        ego = new Object
        support = new Object
        mutate ego, support
    compose:
        do EmergencyMergeEnvironment()
        do EmergencyMergeTraffic()
