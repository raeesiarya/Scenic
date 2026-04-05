from yield_protocol import *

behavior EmergencyMergeHazardPrelude():
    wait

behavior EmergencyMergeHazardPathA():
    do EmergencyMergePrimaryResponse()

behavior EmergencyMergeHazardPathB():
    do EmergencyMergeSecondaryResponse()

scenario EmergencyMergeIncident():
    precondition: True
    invariant: True
    compose:
        do choose {EmergencyMergePrimaryResponse(): 3, EmergencyMergeSecondaryResponse(): 1}
        do shuffle {EmergencyMergeAftershockA(): 2, EmergencyMergeAftershockB(): 1}
