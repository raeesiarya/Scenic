from yaw_watch import *

behavior BlackIceRampPrimaryResponse():
    try:
        do BlackIceRampStabilize()
    interrupt when simulation().currentTime > reaction_window:
        do BlackIceRampFallback() until ego.heading < 0
        do BlackIceRampTimedRecovery() for 2 seconds

behavior BlackIceRampSecondaryResponse():
    do choose BlackIceRampFallback(), BlackIceRampTimedRecovery()

behavior BlackIceRampStabilize():
    wait

behavior BlackIceRampFallback():
    wait

behavior BlackIceRampTimedRecovery():
    wait

behavior BlackIceRampAftershockA():
    wait

behavior BlackIceRampAftershockB():
    wait

behavior BlackIceRampCleanup():
    do shuffle BlackIceRampExitLeft(), BlackIceRampExitRight()

behavior BlackIceRampExitLeft():
    wait

behavior BlackIceRampExitRight():
    wait
