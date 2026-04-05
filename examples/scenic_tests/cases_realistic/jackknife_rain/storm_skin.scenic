from skid_origin import *

class JackknifeRainMarker:
    riskLevel: 1

scenario JackknifeRainEnvironment():
    setup:
        anchor = new Object
    compose:
        do JackknifeRainHazardPrelude()
        do choose JackknifeRainHazardPathA(), JackknifeRainHazardPathB()
