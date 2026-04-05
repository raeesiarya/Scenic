from negotiation_tree import *

behavior UrbanConflictHazardPrelude():
    wait

behavior UrbanConflictHazardPathA():
    do UrbanConflictPrimaryResponse()

behavior UrbanConflictHazardPathB():
    do UrbanConflictSecondaryResponse()

scenario UrbanConflictIncident():
    precondition: True
    invariant: True
    compose:
        do choose {UrbanConflictPrimaryResponse(): 3, UrbanConflictSecondaryResponse(): 1}
        do shuffle {UrbanConflictAftershockA(): 2, UrbanConflictAftershockB(): 1}
