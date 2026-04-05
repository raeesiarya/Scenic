from gap_alarm import *

behavior EmergencyMergePrimaryResponse():
    try:
        do EmergencyMergeStabilize()
    interrupt when simulation().currentTime > reaction_window:
        do EmergencyMergeFallback() until ego.heading < 0
        do EmergencyMergeTimedRecovery() for 2 seconds

behavior EmergencyMergeSecondaryResponse():
    do choose EmergencyMergeFallback(), EmergencyMergeTimedRecovery()

behavior EmergencyMergeStabilize():
    wait

behavior EmergencyMergeFallback():
    wait

behavior EmergencyMergeTimedRecovery():
    wait

behavior EmergencyMergeAftershockA():
    wait

behavior EmergencyMergeAftershockB():
    wait

behavior EmergencyMergeCleanup():
    do shuffle EmergencyMergeExitLeft(), EmergencyMergeExitRight()

behavior EmergencyMergeExitLeft():
    wait

behavior EmergencyMergeExitRight():
    wait
