from helper4 import *
from helper5 import *

behavior WeightedA():
    do Helper4Bridge()

behavior Helper2Leaf():
    take 1

behavior Helper2Shuffle():
    do shuffle Helper4Leaf(), Helper5Leaf()
