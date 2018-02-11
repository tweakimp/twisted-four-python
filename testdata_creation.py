from string import ascii_uppercase


class TFBoard():
    def __init__(self):
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

    # returns list of matrix entries ()
    def flatMatrix(self):
        return [value for array in self.matrix for value in array]

    # draw the board into the console
    def drawBoard(self):
        # colors
        col = ["\033[0m", "\033[91m", "\033[31m", "\033[97m", "\033[92m"]

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