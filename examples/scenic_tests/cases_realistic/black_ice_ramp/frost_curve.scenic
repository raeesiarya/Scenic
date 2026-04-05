from spin_trigger import *

class BlackIceRampMarker:
    riskLevel: 1

scenario BlackIceRampEnvironment():
    setup:
        anchor = new Object
    compose:
        do BlackIceRampHazardPrelude()
        do choose BlackIceRampHazardPathA(), BlackIceRampHazardPathB()
