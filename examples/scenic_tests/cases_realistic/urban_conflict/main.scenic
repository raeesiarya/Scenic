"""Dense urban cyclist-pedestrian conflict realistic stress case."""

from curb_mesh import *
from city_cast import *
from sidewalk_alarm import *

model scenic.simulators.newtonian.model

param severity = 3
param reaction_window = 2

require True
terminate after 60 steps
record initial 1 as 'UrbanConflict_start'
record final 2 as 'UrbanConflict_end'

scenario Main():
    precondition: True
    invariant: True
    setup:
        ego = new Object
        support = new Object
        mutate ego, support
    compose:
        do UrbanConflictEnvironment()
        do UrbanConflictTraffic()
