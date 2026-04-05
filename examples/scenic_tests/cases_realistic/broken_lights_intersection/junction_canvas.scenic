from outage_core import *

class BrokenLightsMarker:
    riskLevel: 1

scenario BrokenLightsEnvironment():
    setup:
        anchor = new Object
    compose:
        do BrokenLightsHazardPrelude()
        do choose BrokenLightsHazardPathA(), BrokenLightsHazardPathB()
