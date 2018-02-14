# import main
import testdata

# for test in testdata.tests:
#     testboard = main.TFBoard()
#     testboard.matrix = test[0]
#     testboard.makeMove(test[1])
#     testboard.checkWin()
#     print(test[2], testboard.endGame)

turnlist = {
    "1": 0,
    "2": 0,
    "3": 0,
    "4": 0,
    "5": 0,
    "6": 0,
    "7": 0,
    "l": 0,
    "r": 0
}
for test in testdata.tests:
    turnlist[test[1]] += 1
print(turnlist)
