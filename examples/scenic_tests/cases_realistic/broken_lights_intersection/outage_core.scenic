from priority_matrix import *

behavior BrokenLightsHazardPrelude():
    wait

behavior BrokenLightsHazardPathA():
    do BrokenLightsPrimaryResponse()

behavior BrokenLightsHazardPathB():
    do BrokenLightsSecondaryResponse()

scenario BrokenLightsIncident():
    precondition: True
    invariant: True
    compose:
        do choose {BrokenLightsPrimaryResponse(): 3, BrokenLightsSecondaryResponse(): 1}
        do shuffle {BrokenLightsAftershockA(): 2, BrokenLightsAftershockB(): 1}
