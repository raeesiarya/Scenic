from spin_trigger import *
from traction_plan import *

scenario BlackIceRampTraffic():
    precondition: True
    invariant: True
    compose:
        do BlackIceRampIncident()
        do BlackIceRampCleanup()
