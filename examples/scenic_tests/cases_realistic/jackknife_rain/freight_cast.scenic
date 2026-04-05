from skid_origin import *
from recovery_lattice import *

scenario JackknifeRainTraffic():
    precondition: True
    invariant: True
    compose:
        do JackknifeRainIncident()
        do JackknifeRainCleanup()
