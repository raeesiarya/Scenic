from traction_plan import *

behavior BlackIceRampHazardPrelude():
    wait

behavior BlackIceRampHazardPathA():
    do BlackIceRampPrimaryResponse()

behavior BlackIceRampHazardPathB():
    do BlackIceRampSecondaryResponse()

scenario BlackIceRampIncident():
    precondition: True
    invariant: True
    compose:
        do choose {BlackIceRampPrimaryResponse(): 3, BlackIceRampSecondaryResponse(): 1}
        do shuffle {BlackIceRampAftershockA(): 2, BlackIceRampAftershockB(): 1}
