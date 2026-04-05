from hydroplane_watch import *

behavior JackknifeRainPrimaryResponse():
    try:
        do JackknifeRainStabilize()
    interrupt when simulation().currentTime > reaction_window:
        do JackknifeRainFallback() until ego.heading < 0
        do JackknifeRainTimedRecovery() for 2 seconds

behavior JackknifeRainSecondaryResponse():
    do choose JackknifeRainFallback(), JackknifeRainTimedRecovery()

behavior JackknifeRainStabilize():
    wait

behavior JackknifeRainFallback():
    wait

behavior JackknifeRainTimedRecovery():
    wait

behavior JackknifeRainAftershockA():
    wait

behavior JackknifeRainAftershockB():
    wait

behavior JackknifeRainCleanup():
    do shuffle JackknifeRainExitLeft(), JackknifeRainExitRight()

behavior JackknifeRainExitLeft():
    wait

behavior JackknifeRainExitRight():
    wait
