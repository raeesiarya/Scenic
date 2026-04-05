from sidewalk_alarm import *

behavior UrbanConflictPrimaryResponse():
    try:
        do UrbanConflictStabilize()
    interrupt when simulation().currentTime > reaction_window:
        do UrbanConflictFallback() until ego.heading < 0
        do UrbanConflictTimedRecovery() for 2 seconds

behavior UrbanConflictSecondaryResponse():
    do choose UrbanConflictFallback(), UrbanConflictTimedRecovery()

behavior UrbanConflictStabilize():
    wait

behavior UrbanConflictFallback():
    wait

behavior UrbanConflictTimedRecovery():
    wait

behavior UrbanConflictAftershockA():
    wait

behavior UrbanConflictAftershockB():
    wait

behavior UrbanConflictCleanup():
    do shuffle UrbanConflictExitLeft(), UrbanConflictExitRight()

behavior UrbanConflictExitLeft():
    wait

behavior UrbanConflictExitRight():
    wait
