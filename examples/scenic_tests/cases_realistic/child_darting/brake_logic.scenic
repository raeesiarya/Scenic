from crosswalk_alarm import *

behavior ChildDartingPrimaryResponse():
    try:
        do ChildDartingStabilize()
    interrupt when simulation().currentTime > reaction_window:
        do ChildDartingFallback() until ego.heading < 0
        do ChildDartingTimedRecovery() for 2 seconds

behavior ChildDartingSecondaryResponse():
    do choose ChildDartingFallback(), ChildDartingTimedRecovery()

behavior ChildDartingStabilize():
    wait

behavior ChildDartingFallback():
    wait

behavior ChildDartingTimedRecovery():
    wait

behavior ChildDartingAftershockA():
    wait

behavior ChildDartingAftershockB():
    wait

behavior ChildDartingCleanup():
    do shuffle ChildDartingExitLeft(), ChildDartingExitRight()

behavior ChildDartingExitLeft():
    wait

behavior ChildDartingExitRight():
    wait
