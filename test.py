matrix = [
    [2, 1, 2, 1, 1, 2, 0],
    [2, 2, 1, 2, 1, 0, 0],
    [1, 2, 2, 0, 0, 0, 0],
    [2, 1, 1, 0, 0, 0, 0],
    [1, 1, 2, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0],
]


def applyGravity(matrix):
    for i in range(7):
        matrix[i] = [x for x in matrix[i] if x != 0]
        matrix[i] += [0 for _ in range(7 - len(matrix[i]))]
    return matrix


def rotateLeft(matrix):
    matrix = list(list(x) for x in zip(*matrix))[::-1]
    matrix = applyGravity(matrix)
    return matrix


def rotateRight(matrix):
    matrix = list(list(x)[::-1] for x in zip(*matrix))
    matrix = applyGravity(matrix)
    return matrix


matrix = rotateRight(matrix)
for x in matrix:
    print(x)
