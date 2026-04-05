from escape_playbook import *

behavior WrongWayFreewayHazardPrelude():
    wait

behavior WrongWayFreewayHazardPathA():
    do WrongWayFreewayPrimaryResponse()

behavior WrongWayFreewayHazardPathB():
    do WrongWayFreewaySecondaryResponse()

scenario WrongWayFreewayIncident():
    precondition: True
    invariant: True
    compose:
        do choose {WrongWayFreewayPrimaryResponse(): 3, WrongWayFreewaySecondaryResponse(): 1}
        do shuffle {WrongWayFreewayAftershockA(): 2, WrongWayFreewayAftershockB(): 1}
