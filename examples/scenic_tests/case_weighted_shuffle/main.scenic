behavior MainBehavior():
    do WeightedShuffle()

behavior WeightedShuffle():
    do shuffle {HeavyLeaf(): 3, LightLeaf(): 1}

behavior HeavyLeaf():
    wait

behavior LightLeaf():
    wait
