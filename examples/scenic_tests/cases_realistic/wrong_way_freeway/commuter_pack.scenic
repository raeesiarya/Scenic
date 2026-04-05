from wrongway_intrusion import *
from escape_playbook import *

scenario WrongWayFreewayTraffic():
    precondition: True
    invariant: True
    compose:
        do WrongWayFreewayIncident()
        do WrongWayFreewayCleanup()
