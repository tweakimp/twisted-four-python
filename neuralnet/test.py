# import cProfile
import pickle
import random
from datetime import datetime

from neuralnet import NEURALNET
from testdata_creation import flatTests

random.seed(1)


def stopwatch(f):
    def wrap(*args, **kw):
        start = datetime.now()
        result = f(*args, **kw)
        end = datetime.now()
        print(end - start)
        return result

    return wrap


def test(net):
    points = 0
    # outcomelist = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for test in testdata:
        outcome = net.feed(test[0])
        # outcomelist[outcome] += 1
        if outcome == 8:
            outcome = "r"
        elif outcome == 7:
            outcome = "l"
        elif outcome <= 6:
            outcome += 1
        if test[1] == outcome:
            points += 1
    # print(f"outcomelist: {outcomelist}")
    # print(f"accuracy: {points*100/len(testdata)}%")
    return points


@stopwatch
def breedtest(length=200, jitter=0.1, accuracy=30):
    global testdata
    testdata = flatTests(length)
    record = 0
    run = 0
    newtests = 0
    nn = NEURALNET()
    with open('current.pickle', 'rb') as loaded:
        nn = pickle.load(loaded)
    while record < (length / 100 * accuracy):
        nochange = 0
        while nochange < 5:
            record = test(nn)
            start = int(record)
            children = nn.breed(jitter, childcount=10)
            for child in children:
                points = test(child)
                if record < points:
                    record = points
                    child.saveState()
                    break
            nochange = nochange + 1 if record == start else 0
            run += 1
            print(
                f"run {run}, accuracy {record}/{length}, no change {nochange}")
            with open('current.pickle', 'rb') as loaded:
                nn = pickle.load(loaded)
        newtests += 1
        print(f"Testloop: {newtests}")
        print(f"Achieved {record*100/length}% accuracy")
        testdata = flatTests(length)


# cProfile.run("breedtest()")

breedtest(1000, 1, 40)
