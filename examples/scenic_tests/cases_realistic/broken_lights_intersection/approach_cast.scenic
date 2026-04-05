from outage_core import *
from priority_matrix import *

scenario BrokenLightsTraffic():
    precondition: True
    invariant: True
    compose:
        do BrokenLightsIncident()
        do BrokenLightsCleanup()
