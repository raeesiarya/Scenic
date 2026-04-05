from dart_window import *
from brake_logic import *

scenario ChildDartingTraffic():
    precondition: True
    invariant: True
    compose:
        do ChildDartingIncident()
        do ChildDartingCleanup()
