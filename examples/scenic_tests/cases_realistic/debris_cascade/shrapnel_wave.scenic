from avoidance_tree import *

behavior DebrisCascadeHazardPrelude():
    wait

behavior DebrisCascadeHazardPathA():
    do DebrisCascadePrimaryResponse()

behavior DebrisCascadeHazardPathB():
    do DebrisCascadeSecondaryResponse()

scenario DebrisCascadeIncident():
    precondition: True
    invariant: True
    compose:
        do choose {DebrisCascadePrimaryResponse(): 3, DebrisCascadeSecondaryResponse(): 1}
        do shuffle {DebrisCascadeAftershockA(): 2, DebrisCascadeAftershockB(): 1}
