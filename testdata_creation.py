import random
from copy import deepcopy
from datetime import datetime
from string import ascii_uppercase


class randomBoard():
    def __init__(self):
        self.width = 7
        self.height = 7
        self.columns = range(1, self.height + 1)
        self.rows = ascii_uppercase[:self.width]
        self.matrix = [[0 for h in range(0, self.height)]
                       for w in range(0, self.width)]
        self.saveMatrix = [[0 for h in range(0, self.height)]
                           for w in range(0, self.width)]
        self.endGame = False
        self.winner = 0
        self.playerTurn = 1
        self.turnNumber = 1

    def flatMatrix(self):
        return [value for array in self.matrix for value in array]

    def putToken(self, player, column):
        for i in range(self.height - 1, -1, -1):
            if i == 0 and self.matrix[column][i] == 0:
                self.matrix[column][0] = player
                return
            if self.matrix[column][i] != 0:
                if i != self.height - 1:
                    self.matrix[column][i + 1] = player
                return

    def checkWin(self):
        for c in range(7):
            column = self.matrix[c]
            for r in range(4):
                start = column[r]
                if start != 0 and all(token == start
                                      for token in column[r:r + 4]):
                    self.endGame = True

        for r in range(self.height - 1, -1, -1):
            row = [self.matrix[c][r] for c in range(7)]
            for c in range(4):
                start = row[c]
                if start != 0 and all(token == start
                                      for token in row[c:c + 4]):
                    self.endGame = True

        for c in range(4):
            for r in range(4):
                diagonal = [self.matrix[c + x][r + x] for x in range(4)]
                start = diagonal[0]
                if start != 0 and all(token == start for token in diagonal):
                    self.endGame = True

        for c in range(4):
            for r in range(3, 7):
                diagonal = [self.matrix[c + x][r - x] for x in range(4)]
                start = diagonal[0]
                if start != 0 and all(token == start for token in diagonal):
                    self.endGame = True

    def checkDraw(self):
        if all(x != 0 for x in self.flatMatrix()):
            return True

    def applyGravity(self):
        for i in range(7):
            self.matrix[i] = [x for x in self.matrix[i] if x != 0]
            self.matrix[i] += [0 for _ in range(7 - len(self.matrix[i]))]

    def rotateLeft(self):
        self.matrix = list(list(x) for x in zip(*self.matrix))[::-1]

    def rotateRight(self):
        self.matrix = list(list(x)[::-1] for x in zip(*self.matrix))

    def possibleMoves(self):
        movelist = ["r", "l"]
        for i in range(len(self.matrix)):
            if 0 in self.matrix[i]:
                movelist.append(i + 1)
        return movelist

    def gameLoop(self):
        while self.endGame is False:
            movelist = self.possibleMoves()
            turn = random.choice(movelist)
            if turn == "L" or turn == "l":
                self.rotateLeft()
                self.applyGravity()
            elif turn == "R" or turn == "r":
                self.rotateRight()
                self.applyGravity()
            elif int(turn) in [1, 2, 3, 4, 5, 6, 7]:
                self.putToken(self.playerTurn, int(turn) - 1)
            self.checkWin()
            if self.endGame is True:
                self.winner = self.playerTurn
                break
            if self.checkDraw():
                break
            self.saveMatrix = deepcopy(self.matrix)
            self.playerTurn = 1 if self.playerTurn == 2 else 2
            self.turnNumber += 1
        return self.saveMatrix, turn, self.playerTurn


def stopwatch(f):
    def wrap(*args, **kw):
        start = datetime.now()
        result = f(*args, **kw)
        end = datetime.now()
        print(end - start)
        return result

    return wrap


def flatMatrix(x):
    return [value for array in x for value in array]


@stopwatch
def createTests(x):
    with open("testdata.py", "w") as testdata:
        testdata.write(f"tests = [\n")
        for n in range(x):
            board = randomBoard()
            saved, turn, player = board.gameLoop()
            if player == 2:
                for i in range(len(saved)):
                    for j in range(len(saved[i])):
                        if saved[i][j] != 0:
                            saved[i][j] = 1 if saved[i][j] == 2 else 2
            testdata.write(f"    [[\n")
            for line in saved:
                testdata.write(f"        {str(line)},\n")
            testdata.write(f"    ], '{str(turn)}', {str(n)}],\n")
        testdata.write("]\n")


@stopwatch
def createFlatTests(x):
    with open("testdata.py", "w") as testdata:
        testdata.write(f"tests = [\n")
        for n in range(x):
            board = randomBoard()
            saved, turn, player = board.gameLoop()
            saved = flatMatrix(saved)
            if player == 2:
                for i in range(len(saved)):
                    if saved[i] != 0:
                        saved[i] = 1 if saved[i] == 2 else 2
            testdata.write(f"    [{str(saved)}, '{str(turn)}', {str(n)}],\n")
        testdata.write("]\n")


createFlatTests(1000)
