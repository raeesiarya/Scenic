from luminance_watch import *

behavior TunnelExitGlarePrimaryResponse():
    try:
        do TunnelExitGlareStabilize()
    interrupt when simulation().currentTime > reaction_window:
        do TunnelExitGlareFallback() until ego.heading < 0
        do TunnelExitGlareTimedRecovery() for 2 seconds

behavior TunnelExitGlareSecondaryResponse():
    do choose TunnelExitGlareFallback(), TunnelExitGlareTimedRecovery()

behavior TunnelExitGlareStabilize():
    wait

behavior TunnelExitGlareFallback():
    wait

behavior TunnelExitGlareTimedRecovery():
    wait

behavior TunnelExitGlareAftershockA():
    wait

behavior TunnelExitGlareAftershockB():
    wait

behavior TunnelExitGlareCleanup():
    do shuffle TunnelExitGlareExitLeft(), TunnelExitGlareExitRight()

behavior TunnelExitGlareExitLeft():
    wait

behavior TunnelExitGlareExitRight():
    wait
