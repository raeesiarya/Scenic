from dart_window import *

class ChildDartingMarker:
    riskLevel: 1

scenario ChildDartingEnvironment():
    setup:
        anchor = new Object
    compose:
        do ChildDartingHazardPrelude()
        do choose ChildDartingHazardPathA(), ChildDartingHazardPathB()
