from siren_corridor import *

class EmergencyMergeMarker:
    riskLevel: 1

scenario EmergencyMergeEnvironment():
    setup:
        anchor = new Object
    compose:
        do EmergencyMergeHazardPrelude()
        do choose EmergencyMergeHazardPathA(), EmergencyMergeHazardPathB()
