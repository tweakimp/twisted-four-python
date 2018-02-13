import main
import testdata

for test in testdata.tests:
    testboard = main.TFBoard()
    testboard.matrix = test[0]
    testboard.makeMove(test[1])
    testboard.checkWin()
    print(test[2], testboard.endGame)
