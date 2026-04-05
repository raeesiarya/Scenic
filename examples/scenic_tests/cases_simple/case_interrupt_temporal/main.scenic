behavior MainBehavior():
    try:
        do BaseBehavior()
    interrupt when simulation().currentTime > 1:
        do InterruptBehavior() until ego.heading < 0
        do TimedBehavior() for 3 seconds

behavior BaseBehavior():
    wait

behavior InterruptBehavior():
    wait

behavior TimedBehavior():
    wait
