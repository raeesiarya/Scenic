"""Child darting out between parked cars realistic stress case."""

from curb_shadow import *
from street_cast import *
from crosswalk_alarm import *

model scenic.simulators.newtonian.model

param severity = 3
param reaction_window = 2

require True
terminate after 60 steps
record initial 1 as 'ChildDarting_start'
record final 2 as 'ChildDarting_end'

scenario Main():
    precondition: True
    invariant: True
    setup:
        ego = new Object
        support = new Object
        mutate ego, support
    compose:
        do ChildDartingEnvironment()
        do ChildDartingTraffic()
