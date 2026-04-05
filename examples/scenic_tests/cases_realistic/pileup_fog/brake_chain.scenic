from evasive_weave import *

behavior PileupFogHazardPrelude():
    wait

behavior PileupFogHazardPathA():
    do PileupFogPrimaryResponse()

behavior PileupFogHazardPathB():
    do PileupFogSecondaryResponse()

scenario PileupFogIncident():
    precondition: True
    invariant: True
    compose:
        do choose {PileupFogPrimaryResponse(): 3, PileupFogSecondaryResponse(): 1}
        do shuffle {PileupFogAftershockA(): 2, PileupFogAftershockB(): 1}
