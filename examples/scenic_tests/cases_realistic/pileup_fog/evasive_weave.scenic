from visibility_alarm import *

behavior PileupFogPrimaryResponse():
    try:
        do PileupFogStabilize()
    interrupt when simulation().currentTime > reaction_window:
        do PileupFogFallback() until ego.heading < 0
        do PileupFogTimedRecovery() for 2 seconds

behavior PileupFogSecondaryResponse():
    do choose PileupFogFallback(), PileupFogTimedRecovery()

behavior PileupFogStabilize():
    wait

behavior PileupFogFallback():
    wait

behavior PileupFogTimedRecovery():
    wait

behavior PileupFogAftershockA():
    wait

behavior PileupFogAftershockB():
    wait

behavior PileupFogCleanup():
    do shuffle PileupFogExitLeft(), PileupFogExitRight()

behavior PileupFogExitLeft():
    wait

behavior PileupFogExitRight():
    wait
