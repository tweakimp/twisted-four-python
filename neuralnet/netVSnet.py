from string import ascii_uppercase
import pickle


class TFBoard():
    def __init__(self, net1, net2):
        self.width = 7
        self.height = 7
        # lists from 1 to 7 and A to G for board labels
        self.columns = range(1, self.height + 1)
        self.rows = ascii_uppercase[:self.width]
        # matrix that contains the game state data, initialized with 0s
        self.matrix = [[0 for h in range(0, self.height)]
                       for w in range(0, self.width)]
        # start values for the game
        self.endGame = False
        self.winner = 0
        self.playerTurn = 1
        self.turnNumber = 1
        self.net1 = net1
        self.net2 = net2

    # returns list of matrix entries ()
    def flatMatrix(self):
        return [value for array in self.matrix for value in array]

    # draw the board into the console
    def drawBoard(self):
        def drawInLoops(i, j):
            if i == self.height:
                if j == 0:
                    # bottom left corner
                    print("   ", end=f"")
                else:
                    # bottom letter row
                    print(f"{self.columns[j-1]}", end=f"  ")
            else:
                if j == 0:
                    # left number column
                    print(f"{self.rows[-i-1]}", end=" ")
                else:
                    # squares
                    # drawn matrix is 1 higher and wider than self.matrix
                    print(f"[", end="")
                    piece = self.matrix[j - 1][self.height - i - 1]
                    if piece == 1:
                        piece = f"X"
                    elif piece == 2:
                        piece = f"O"
                    elif piece == 0:
                        piece = " "
                    print(f"{piece}", end="")
                    print(f"]", end="")

        for i in range(0, self.height + 1):
            for j in range(0, self.width + 1):
                drawInLoops(i, j)
            print("")
        print("")  # new line after board for better looks

    # put token into a column
    def putToken(self, player, column):
        # find first nonzero entrie in column from top
        notification = f"New Player {player} token in column {column+1}"
        for i in range(self.height - 1, -1, -1):
            if i == 0 and self.matrix[column][i] == 0:
                self.matrix[column][0] = player
                print(f"{notification}, row {self.rows[i]}")
                return
            if self.matrix[column][i] != 0:
                if i == self.height - 1:
                    print(f"COLUMN FULL!\nCan\'t place token in column {i}.")
                else:
                    self.matrix[column][i + 1] = player
                    print(f"{notification}, row {self.rows[i+1]}")
                return

        def possbileMoves(self):
            movelist = ["r", "R", "l", "L"]
            for i in range(len(self.matrix)):
                if 0 in self.matrix[i]:
                    movelist.append(i)
            return movelist

    def checkWin(self):
        # check for win by column
        def checkColumns():
            # go through columns
            for c in range(7):
                column = self.matrix[c]
                for r in range(4):
                    # start points r
                    start = column[r]
                    if start != 0 and all(token == start
                                          for token in column[r:r + 4]):
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
                    if start != 0 and all(token == start
                                          for token in row[c:c + 4]):
                        print(f"Win by row for player {start}")
                        print(f"{self.rows[r]}{c+1}-{self.rows[r]}{c+4}")
                        self.endGame = True

        def checkbltrDiagonals():
            for c in range(4):
                for r in range(4):
                    diagonal = [self.matrix[c + x][r + x] for x in range(4)]
                    start = diagonal[0]
                    if start != 0 and all(token == start
                                          for token in diagonal):
                        print(f"Win by diagonal bltr for player {start}")
                        print(f"{self.rows[r]}{c+1}-{self.rows[r+3]}{c+4}")
                        self.endGame = True

        def checktlbrDiagonals():
            for c in range(4):
                for r in range(3, 7):
                    diagonal = [self.matrix[c + x][r - x] for x in range(4)]
                    start = diagonal[0]
                    if start != 0 and all(token == start
                                          for token in diagonal):
                        print(f"Win by diagonal tlbr for player {start}")
                        print(f"{self.rows[r]}{c+1}-{self.rows[r-3]}{c+4}")
                        self.endGame = True

        checkColumns()
        checkRows()
        checktlbrDiagonals()
        checkbltrDiagonals()

    # draw if all spots are not 0
    def checkDraw(self):
        if all(x != 0 for x in self.flatMatrix()):
            return True

    # lets tokens fall down
    def applyGravity(self):
        for i in range(7):
            self.matrix[i] = [x for x in self.matrix[i] if x != 0]
            self.matrix[i] += [0 for _ in range(7 - len(self.matrix[i]))]

    def rotateLeft(self):
        self.matrix = list(list(x) for x in zip(*self.matrix))[::-1]

    def rotateRight(self):
        self.matrix = list(list(x)[::-1] for x in zip(*self.matrix))

    def makeMove(self, turn):
        if turn == "L" or turn == "l":
            self.rotateLeft()
            self.applyGravity()
        elif turn == "R" or turn == "r":
            self.rotateRight()
            self.applyGravity()
        elif int(turn) in [1, 2, 3, 4, 5, 6, 7]:
            self.putToken(self.playerTurn, int(turn) - 1)

    # actual game loop
    def gameLoop(self):
        print("---NEW GAME")
        self.drawBoard()
        # as long as game is not ended:
        # each while loop is a turn
        while self.endGame is False:
            print(f"---Turn {self.turnNumber}:")
            if self.playerTurn == 1:
                nnboard = self.flatMatrix()
                for x in nnboard:
                    x = x if x == 0 or x == 1 else -1
                turn = nn.feed(nnboard)
            elif self.playerTurn == 2:
                turn = input(
                    f"Player {self.playerTurn}, make your move.\n(1,2,3,4,5,6,7,L,R)\n---"
                )
                if turn not in [
                        "1", "2", "3", "4", "5", "6", "7", "l", "L", "r", "R"
                ]:
                    print(
                        f"WRONG INPUT {turn}!\nInput must be L, R or an integer between 1 and 7."
                    )
                    continue  # restart turn (playerTurn is not changed)
            # turn changes the board
            self.makeMove(turn)
            # check for wins
            self.checkWin()
            if self.endGame is True:
                self.winner = self.playerTurn
                break
            # check for draws
            if self.checkDraw():
                break
            # end turn by changing player turn, increasing turn number
            # and draw the current board
            self.playerTurn = 1 if self.playerTurn == 2 else 2
            self.turnNumber += 1
            self.drawBoard()
        if self.winner == 0:
            print(f"DRAW!")
        else:
            print(f"Player {self.winner} won in {self.turnNumber} turns!")
        self.drawBoard()
        return self.winner


with open('net1.pickle', 'rb') as loaded:
    n1 = pickle.load(loaded)
with open('net2.pickle', 'rb') as loaded:
    n2 = pickle.load(loaded)

board = TFBoard(n1, n2)
board.gameLoop()