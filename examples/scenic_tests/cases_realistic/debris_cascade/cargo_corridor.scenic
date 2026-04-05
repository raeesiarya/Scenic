from shrapnel_wave import *

class DebrisCascadeMarker:
    riskLevel: 1

scenario DebrisCascadeEnvironment():
    setup:
        anchor = new Object
    compose:
        do DebrisCascadeHazardPrelude()
        do choose DebrisCascadeHazardPathA(), DebrisCascadeHazardPathB()
