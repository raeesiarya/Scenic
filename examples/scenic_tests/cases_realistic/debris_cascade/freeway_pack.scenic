from shrapnel_wave import *
from avoidance_tree import *

scenario DebrisCascadeTraffic():
    precondition: True
    invariant: True
    compose:
        do DebrisCascadeIncident()
        do DebrisCascadeCleanup()
