from siren_corridor import *
from yield_protocol import *

scenario EmergencyMergeTraffic():
    precondition: True
    invariant: True
    compose:
        do EmergencyMergeIncident()
        do EmergencyMergeCleanup()
