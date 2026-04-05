"""Tunnel exit glare with stopped vehicle realistic stress case."""

from tunnel_shell import *
from approach_convoy import *
from luminance_watch import *

model scenic.simulators.newtonian.model

param severity = 3
param reaction_window = 2

require True
terminate after 60 steps
record initial 1 as 'TunnelExitGlare_start'
record final 2 as 'TunnelExitGlare_end'

scenario Main():
    precondition: True
    invariant: True
    setup:
        ego = new Object
        support = new Object
        mutate ego, support
    compose:
        do TunnelExitGlareEnvironment()
        do TunnelExitGlareTraffic()
