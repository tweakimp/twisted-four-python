# import cProfile
import pickle
from datetime import datetime

from netVSnet import TFBoard
from neuralnet import NEURALNET


def stopwatch(f):
    def wrap(*args, **kw):
        start = datetime.now()
        result = f(*args, **kw)
        end = datetime.now()
        print(end - start)
        return result

    return wrap


@stopwatch
def breedtest(jitter, childcount):
    run = 0
    # mother = NEURALNET()
    with open('current.pickle', 'rb') as loaded:
        mother = pickle.load(loaded)
    while True:
        nets = [mother] + mother.breed(jitter, childcount)
        length = len(nets)
        points = [0 for x in range(length)]
        for i in range(length):
            for j in range(length):
                if i != j:
                    board = TFBoard()
                    winner, _ = board.gameLoop(nets[i], nets[j])
                    if winner == 0:
                        points[i] += -1
                        points[j] += -1
                    elif winner == 1:
                        points[i] += 2
                        points[j] += -2
                    elif winner == 2:
                        points[i] += -2
                        points[j] += 2
        mother = nets[points.index(max(points))]
        run += 1
        print(f"run {run}, points {max(points)}/{4*(length-1)}")
        with open('mother.pickle', 'wb') as handle:
            pickle.dump(mother, handle, protocol=pickle.HIGHEST_PROTOCOL)


breedtest(0.2, 10)
