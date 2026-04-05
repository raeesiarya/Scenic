from glare_burst import *
from escape_routine import *

scenario TunnelExitGlareTraffic():
    precondition: True
    invariant: True
    compose:
        do TunnelExitGlareIncident()
        do TunnelExitGlareCleanup()
