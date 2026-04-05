from clearance_watch import *

behavior DebrisCascadePrimaryResponse():
    try:
        do DebrisCascadeStabilize()
    interrupt when simulation().currentTime > reaction_window:
        do DebrisCascadeFallback() until ego.heading < 0
        do DebrisCascadeTimedRecovery() for 2 seconds

behavior DebrisCascadeSecondaryResponse():
    do choose DebrisCascadeFallback(), DebrisCascadeTimedRecovery()

behavior DebrisCascadeStabilize():
    wait

behavior DebrisCascadeFallback():
    wait

behavior DebrisCascadeTimedRecovery():
    wait

behavior DebrisCascadeAftershockA():
    wait

behavior DebrisCascadeAftershockB():
    wait

behavior DebrisCascadeCleanup():
    do shuffle DebrisCascadeExitLeft(), DebrisCascadeExitRight()

behavior DebrisCascadeExitLeft():
    wait

behavior DebrisCascadeExitRight():
    wait
