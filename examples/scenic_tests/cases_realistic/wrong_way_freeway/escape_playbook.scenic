from closure_watch import *

behavior WrongWayFreewayPrimaryResponse():
    try:
        do WrongWayFreewayStabilize()
    interrupt when simulation().currentTime > reaction_window:
        do WrongWayFreewayFallback() until ego.heading < 0
        do WrongWayFreewayTimedRecovery() for 2 seconds

behavior WrongWayFreewaySecondaryResponse():
    do choose WrongWayFreewayFallback(), WrongWayFreewayTimedRecovery()

behavior WrongWayFreewayStabilize():
    wait

behavior WrongWayFreewayFallback():
    wait

behavior WrongWayFreewayTimedRecovery():
    wait

behavior WrongWayFreewayAftershockA():
    wait

behavior WrongWayFreewayAftershockB():
    wait

behavior WrongWayFreewayCleanup():
    do shuffle WrongWayFreewayExitLeft(), WrongWayFreewayExitRight()

behavior WrongWayFreewayExitLeft():
    wait

behavior WrongWayFreewayExitRight():
    wait
