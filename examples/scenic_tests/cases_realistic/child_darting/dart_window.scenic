from brake_logic import *

behavior ChildDartingHazardPrelude():
    wait

behavior ChildDartingHazardPathA():
    do ChildDartingPrimaryResponse()

behavior ChildDartingHazardPathB():
    do ChildDartingSecondaryResponse()

scenario ChildDartingIncident():
    precondition: True
    invariant: True
    compose:
        do choose {ChildDartingPrimaryResponse(): 3, ChildDartingSecondaryResponse(): 1}
        do shuffle {ChildDartingAftershockA(): 2, ChildDartingAftershockB(): 1}
