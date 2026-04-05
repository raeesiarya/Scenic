from brake_chain import *

class PileupFogMarker:
    riskLevel: 1

scenario PileupFogEnvironment():
    setup:
        anchor = new Object
    compose:
        do PileupFogHazardPrelude()
        do choose PileupFogHazardPathA(), PileupFogHazardPathB()
