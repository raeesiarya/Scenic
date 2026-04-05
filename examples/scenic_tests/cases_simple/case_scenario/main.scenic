from helper1 import *

scenario Main():
    setup:
        ego = new Object
    compose:
        do ImportedScenario()
        do choose LocalScenario(), AlternateScenario()

scenario LocalScenario():
    compose:
        do LocalBehavior()

scenario AlternateScenario():
    compose:
        do LocalBehavior()

behavior LocalBehavior():
    wait
