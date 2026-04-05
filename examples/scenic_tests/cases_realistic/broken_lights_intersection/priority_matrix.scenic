from rightofway_watch import *

behavior BrokenLightsPrimaryResponse():
    try:
        do BrokenLightsStabilize()
    interrupt when simulation().currentTime > reaction_window:
        do BrokenLightsFallback() until ego.heading < 0
        do BrokenLightsTimedRecovery() for 2 seconds

behavior BrokenLightsSecondaryResponse():
    do choose BrokenLightsFallback(), BrokenLightsTimedRecovery()

behavior BrokenLightsStabilize():
    wait

behavior BrokenLightsFallback():
    wait

behavior BrokenLightsTimedRecovery():
    wait

behavior BrokenLightsAftershockA():
    wait

behavior BrokenLightsAftershockB():
    wait

behavior BrokenLightsCleanup():
    do shuffle BrokenLightsExitLeft(), BrokenLightsExitRight()

behavior BrokenLightsExitLeft():
    wait

behavior BrokenLightsExitRight():
    wait
