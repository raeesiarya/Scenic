from helper1 import *

behavior MainBehavior():
    do LocalStart()
    do ImportedChain()
    do TailShuffle()

behavior LocalStart():
    do choose LocalLeft(), LocalRight()

behavior LocalLeft():
    take 1

behavior LocalRight():
    take 1

behavior TailShuffle():
    do shuffle TailA(), TailB()

behavior TailA():
    take 1

behavior TailB():
    take 1
