from glare_burst import *

class TunnelExitGlareMarker:
    riskLevel: 1

scenario TunnelExitGlareEnvironment():
    setup:
        anchor = new Object
    compose:
        do TunnelExitGlareHazardPrelude()
        do choose TunnelExitGlareHazardPathA(), TunnelExitGlareHazardPathB()
