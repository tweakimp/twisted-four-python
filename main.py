import random
from string import ascii_uppercase


class TFBoard():
    def __init__(self):
        self.width = 7
        self.height = 7
        self.columns = range(1, self.height + 1)
        self.rows = ascii_uppercase[:self.width]
        self.matrix = [[0 for h in range(0, self.height)]
                       for w in range(0, self.width)]
        self.endGame = False
        self.winner = 0
        self.playerTurn = 1
        self.turnNumber = 1

    def flatMatrix(self):
        return [value for array in self.matrix for value in array]

    def drawBoard(self):
        col = ["\033[0m", "\033[91m", "\033[31m", "\033[97m", "\033[92m"]
        #        no color    lightred      red         white       green

        def drawInLoops(i, j):
            if i == self.height:
                if j == 0:
                    # bottom left corner
                    print("   ", end=f"")
                else:
                    # bottom letter row
                    print(f"{col[1]}{self.columns[j-1]}{col[0]}", end=f"  ")
            else:
                if j == 0:
                    # left number column
                    print(f"{col[1]}{self.rows[-i-1]}{col[0]}", end=" ")
                else:
                    # squares
                    # drawn matrix is 1 higher and wider than self.matrix
                    print(f"{col[2]}[{col[0]}", end="")
                    piece = self.matrix[j - 1][self.height - i - 1]
                    if piece == 1:
                        piece = f"{col[3]}X{col[0]}"
                    elif piece == 2:
                        piece = f"{col[4]}O{col[0]}"
                    elif piece == 0:
                        piece = " "
                    print(f"{piece}", end="")
                    print(f"{col[2]}]{col[0]}", end="")
        for i in range(0, self.height + 1):
            for j in range(0, self.width + 1):
                drawInLoops(i, j)
            print("")
        print("")  # new line after board for better looks

    def putToken(self, player, column):
        # find first nonzero entrie in column from top
        notification = f"New Player {player} token in column {column+1}"
        for i in range(self.height - 1, -1, -1):
            if i == 0 and board.matrix[column][i] == 0:
                self.matrix[column][0] = player
                print(f"{notification}, row {self.rows[i]}")
                return
            if board.matrix[column][i] != 0:
                if i == self.height - 1:
                    print(f"COLUMN FULL!\nCan\'t place token in column {i}.")
                else:
                    self.matrix[column][i + 1] = player
                    print(f"{notification}, row {self.rows[i+1]}")
                return

    def checkWin(self):
        # check for win by column
        def checkColumns():
            # go through columns
            for c in range(7):
                column = self.matrix[c]
                for r in range(4):
                    # start points r
                    start = column[r]
                    if start != 0 and all(token == start for token in column[r:r + 4]):
                        print(f"Win by column for player {start}")
                        print(f"{self.rows[r]}{c+1}-{self.rows[r+3]}{c+1}")
                        self.endGame = True
        # check for win by row

        def checkRows():
            # go through rows
            for r in range(self.height - 1, -1, -1):
                # write rows as lists
                row = [self.matrix[c][r] for c in range(7)]
                for c in range(4):
                    start = row[c]
                    if start != 0 and all(token == start for token in row[c:c + 4]):
                        print(f"Win by row for player {start}")
                        print(f"{self.rows[r]}{c+1}-{self.rows[r]}{c+4}")
                        self.endGame = True

        def checkbltrDiagonals():
            for c in range(4):
                for r in range(4):
                    diagonal = [self.matrix[c + x][r + x] for x in range(4)]
                    start = diagonal[0]
                    if start != 0 and all(token == start for token in diagonal):
                        print(f"Win by diagonal bltr for player {start}")
                        print(f"{self.rows[r]}{c+1}-{self.rows[r+3]}{c+4}")
                        self.endGame = True

        def checktlbrDiagonals():
            for c in range(4):
                for r in range(3, 7):
                    diagonal = [self.matrix[c + x][r - x] for x in range(4)]
                    start = diagonal[0]
                    if start != 0 and all(token == start for token in diagonal):
                        print(f"Win by diagonal tlbr for player {start}")
                        print(f"{self.rows[r]}{c+1}-{self.rows[r-3]}{c+4}")
                        self.endGame = True

        checkColumns()
        checkRows()
        checktlbrDiagonals()
        checkbltrDiagonals()

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

    def gameLoop(self):
        playerTurn = 1
        print("---NEW GAME")
        self.drawBoard()
        while self.endGame is False:
            print(f"---Turn {self.turnNumber}:")
            turn = input(f"Player {playerTurn}, make your move.\n(1,2,3,4,5,6,7,L,R)\n---")
            if turn not in ["1", "2", "3", "4", "5", "6", "7", "l", "L", "r", "R"]:
                print(f"WRONG INPUT {turn}!\nInput must be L, R or an integer between 1 and 7.")
                continue
            if turn == "L" or turn == "l":
                self.rotateLeft()
                self.applyGravity()
            elif turn == "R" or turn == "r":
                self.rotateRight()
                self.applyGravity()
            elif int(turn) in [1, 2, 3, 4, 5, 6, 7]:
                self.putToken(playerTurn, int(turn) - 1)
            self.checkWin()
            if self.endGame is True:
                self.Winner = playerTurn
                break
            if self.checkDraw():
                break
            playerTurn = 1 if playerTurn == 2 else 2
            self.turnNumber += 1
            self.drawBoard()
            print(self.flatMatrix())
        if self.winner == 0:
            print(f"DRAW!")
        else:
            print(f"Player {self.Winner} won in {self.turnNumber} turns!")
        self.drawBoard()


if __name__ == '__main__':
    testMatrix = [[1, 0, 0, 0, 0, 0, 0],
                  [2, 0, 0, 0, 0, 0, 0],
                  [2, 0, 0, 0, 0, 0, 0],
                  [1, 2, 2, 0, 0, 0, 0],
                  [2, 0, 0, 0, 0, 0, 0],
                  [1, 0, 0, 0, 0, 0, 0],
                  [1, 1, 0, 0, 0, 0, 0]]

    randomMatrix = [[random.choice((0, 1, 2)) for _ in range(7)] for _ in range(7)]
    board = TFBoard()
    board.gameLoop()
