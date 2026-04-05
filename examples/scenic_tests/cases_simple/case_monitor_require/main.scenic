monitor SafetyMonitor(limit=5):
    wait

require monitor SafetyMonitor(limit=3)

behavior MainBehavior():
    do BranchBehavior()

behavior BranchBehavior():
    do choose LeafA(), LeafB()

behavior LeafA():
    wait

behavior LeafB():
    wait
