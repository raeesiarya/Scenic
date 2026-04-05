from conflict_weave import *
from negotiation_tree import *

scenario UrbanConflictTraffic():
    precondition: True
    invariant: True
    compose:
        do UrbanConflictIncident()
        do UrbanConflictCleanup()
