"""Wrong-way driver on freeway realistic stress case."""

from median_state import *
from commuter_pack import *
from closure_watch import *

model scenic.simulators.newtonian.model

param severity = 3
param reaction_window = 2

require True
terminate after 60 steps
record initial 1 as 'WrongWayFreeway_start'
record final 2 as 'WrongWayFreeway_end'

scenario Main():
    precondition: True
    invariant: True
    setup:
        ego = new Object
        support = new Object
        mutate ego, support
    compose:
        do WrongWayFreewayEnvironment()
        do WrongWayFreewayTraffic()
