import pickle
import random
from copy import deepcopy

from math import exp

# create matrix of size f*s, initialized with randomFloat() entries
# with f, s sizes of first and second layer


def createRandomWeights(firstlayer, secondlayer):
    return [[randomFloat(-1, 1) for x in range(firstlayer.size)]
            for y in range(secondlayer.size)]


# normalize x to be a value between 0 and 1
def normcombo(x):
    return 0 if x <= 0 else 1 / (1 + exp(-x))


def normlogi(x):
    return 1 / (1 + exp(-x))


def normrect(x):
    return 0 if x <= 0 else x


# create a random float number between -5 and 5# create a random float number between -5 and 5
def randomFloat(lower, upper):
    return random.uniform(lower, upper)


def randomChange(jitter):
    return random.gauss(0, jitter)


# layer class, input size
# creates value list of that size
# creates bias list of that size, initialized with randomFloat() entries
class LAYER():
    def __init__(self, size, methodnorm):
        self.size = size
        self.values = [0 for _ in range(self.size)]
        self.biases = [randomFloat(-2, 0) for _ in range(self.size)]
        self.methodnorm = methodnorm

    # for each value of layer, sum products of weight and input of the
    # corresponsing input values and weightMatrix weights
    # change layer values to be the normalized sum
    def propagate(self, incomingLayer, weightMatrix):
        for i in range(self.size):
            current = 0
            for j in range(incomingLayer.size):
                current += incomingLayer.values[j] * weightMatrix[i][j]
            if self.methodnorm == "rect":
                self.values[i] = normrect(self.biases[i] + current)
            elif self.methodnorm == "logi":
                self.values[i] = normlogi(self.biases[i] + current)
            elif self.methodnorm == "combo":
                self.values[i] = normcombo(self.biases[i] + current)
            else:
                print("INVALID PROPGATE METHOD CHOSEN!")
                raise SystemExit


# neural net class
# initializes 5 layers, creates the random weights between them
class NEURALNET():
    def __init__(self):
        self.sizes = {
            "input": 147,
            "hidden1": 50,
            "hidden2": 50,
            "hidden3": 50,
            "output": 9
        }

        self.inputlayer = LAYER(self.sizes["input"], "logi")
        self.hidden1 = LAYER(self.sizes["hidden1"], "logi")
        self.hidden2 = LAYER(self.sizes["hidden2"], "logi")
        self.hidden3 = LAYER(self.sizes["hidden3"], "logi")
        self.outputlayer = LAYER(self.sizes["output"], "combo")

        self.in_h1_weights = createRandomWeights(self.inputlayer, self.hidden1)
        self.h1_h2_weights = createRandomWeights(self.hidden1, self.hidden2)
        self.h2_h3_weights = createRandomWeights(self.hidden2, self.hidden3)
        self.h3_out_weights = createRandomWeights(self.hidden3,
                                                  self.outputlayer)

    # feeds incoming data through the net, calculating the values of the
    # following layer and ultimately giving the index of the output
    # neuron with the largest value
    def feed(self, inputdata, possibleMoves):
        self.inputlayer.values = [0 for x in self.inputlayer.values]
        # input data (3 values for each game cell version)
        for i in range(len(inputdata)):
            if inputdata[i] == 0:
                self.inputlayer.values[i] = 1
            elif inputdata[i] == 1:
                self.inputlayer.values[i + 49] = 1
            elif inputdata[i] == -1:
                self.inputlayer.values[i + 98] = 1
        # # input data ( 1 value for each game cell version)
        # for i in range(self.inputlayer.size):
        #     self.inputlayer.values[i] = normalize(
        #         self.inputlayer.biases[i] + inputdata[i])
        # input to h1
        self.hidden1.propagate(self.inputlayer, self.in_h1_weights)
        # h1 to h2
        self.hidden2.propagate(self.hidden1, self.h1_h2_weights)
        # h2 to h3
        self.hidden3.propagate(self.hidden2, self.h2_h3_weights)
        # h3 to output
        self.outputlayer.propagate(self.hidden3, self.h3_out_weights)
        # output
        for i in range(len(self.outputlayer.values)):
            self.outputlayer.values[
                i] = -1 if i not in possibleMoves else self.outputlayer.values[
                    i]
        return self.outputlayer.values.index(max(self.outputlayer.values))

    def saveState(self, name="current"):
        with open(f"{name}.pickle", "wb") as file:
            pickle.dump(self, file, pickle.HIGHEST_PROTOCOL)

    def breed(self, jitter=0.1, childcount=10):
        children = []
        for _ in range(1, childcount + 1):
            child = deepcopy(self)
            child.inputlayer.biases = [
                x + randomChange(jitter) for x in child.inputlayer.biases
            ]
            child.hidden1.biases = [
                x + randomChange(jitter) for x in child.hidden1.biases
            ]
            child.hidden2.biases = [
                x + randomChange(jitter) for x in child.hidden2.biases
            ]
            child.hidden3.values = [
                x + randomChange(jitter) for x in child.hidden3.values
            ]
            child.outputlayer.biases = [
                x + randomChange(jitter) for x in child.outputlayer.biases
            ]
            child.in_h1_weights = [[x + randomChange(jitter) for x in y]
                                   for y in child.in_h1_weights]
            child.h1_h2_weights = [[x + randomChange(jitter) for x in y]
                                   for y in child.h1_h2_weights]
            child.h2_h3_weights = [[x + randomChange(jitter) for x in y]
                                   for y in child.h2_h3_weights]
            child.h3_out_weights = [[x + randomChange(jitter) for x in y]
                                    for y in child.h3_out_weights]

            children.append(child)
        return children
