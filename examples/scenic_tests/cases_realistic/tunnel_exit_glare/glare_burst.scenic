from escape_routine import *

behavior TunnelExitGlareHazardPrelude():
    wait

behavior TunnelExitGlareHazardPathA():
    do TunnelExitGlarePrimaryResponse()

behavior TunnelExitGlareHazardPathB():
    do TunnelExitGlareSecondaryResponse()

scenario TunnelExitGlareIncident():
    precondition: True
    invariant: True
    compose:
        do choose {TunnelExitGlarePrimaryResponse(): 3, TunnelExitGlareSecondaryResponse(): 1}
        do shuffle {TunnelExitGlareAftershockA(): 2, TunnelExitGlareAftershockB(): 1}
