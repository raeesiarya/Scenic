from recovery_lattice import *

behavior JackknifeRainHazardPrelude():
    wait

behavior JackknifeRainHazardPathA():
    do JackknifeRainPrimaryResponse()

behavior JackknifeRainHazardPathB():
    do JackknifeRainSecondaryResponse()

scenario JackknifeRainIncident():
    precondition: True
    invariant: True
    compose:
        do choose {JackknifeRainPrimaryResponse(): 3, JackknifeRainSecondaryResponse(): 1}
        do shuffle {JackknifeRainAftershockA(): 2, JackknifeRainAftershockB(): 1}
