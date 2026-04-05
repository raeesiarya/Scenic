from wrongway_intrusion import *

class WrongWayFreewayMarker:
    riskLevel: 1

scenario WrongWayFreewayEnvironment():
    setup:
        anchor = new Object
    compose:
        do WrongWayFreewayHazardPrelude()
        do choose WrongWayFreewayHazardPathA(), WrongWayFreewayHazardPathB()
