from brake_chain import *
from evasive_weave import *

scenario PileupFogTraffic():
    precondition: True
    invariant: True
    compose:
        do PileupFogIncident()
        do PileupFogCleanup()
