from helper1 import *

behavior MainBehavior():
    do LocalBranch()
    do ImportedBranch()
    do ShuffleTail()

behavior LocalBranch():
    do choose LocalA(), LocalB()

behavior LocalA():
    do LocalLeaf()

behavior LocalB():
    do LocalLeaf()

behavior LocalLeaf():
    take 1

behavior ShuffleTail():
    do shuffle TailA(), TailB()

behavior TailA():
    take 1

behavior TailB():
    take 1
