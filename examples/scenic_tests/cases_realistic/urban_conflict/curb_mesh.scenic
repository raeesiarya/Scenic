from conflict_weave import *

class UrbanConflictMarker:
    riskLevel: 1

scenario UrbanConflictEnvironment():
    setup:
        anchor = new Object
    compose:
        do UrbanConflictHazardPrelude()
        do choose UrbanConflictHazardPathA(), UrbanConflictHazardPathB()
