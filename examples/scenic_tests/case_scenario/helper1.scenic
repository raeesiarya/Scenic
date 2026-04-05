behavior ImportedBehavior():
    do ImportedLeaf()

scenario ImportedScenario():
    compose:
        do ImportedBehavior()

behavior ImportedLeaf():
    wait
