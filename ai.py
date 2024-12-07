from utils import gameOver
from utils import INF
from eval import evaluatePosition
def minimax(grid, size, depth, isMax):
    result = gameOver(grid, size)
    if depth == 0 or result != -1:
        if result == 1:
            return INF, None
        if result == 2:
            return -INF, None
        if result == 0:
            return 0, None
        return evaluatePosition(grid, size, isMax), None

    bestMove = [-1, -1]
    if isMax:
        maxScore = -INF
        for i in range(size):
            for j in range(size):
                if grid[i][j] == 0:
                    grid[i][j] = 1
                    score, _ = minimax(grid, size, depth - 1, False)
                    grid[i][j] = 0
                    if(score > maxScore):
                        maxScore, bestMove = score, [i, j]
        return maxScore, bestMove
    else:
        minScore = INF
        for i in range(size):
            for j in range(size):
                if grid[i][j] == 0:
                    grid[i][j] = 2
                    score, _ = minimax(grid, size, depth - 1, True)
                    grid[i][j] = 0
                    if(score < minScore):
                        minScore, bestMove = score, [i, j]
        return minScore, bestMove

def moveAI(grid, size, depth):
    _, move = minimax(grid, size, depth, True)
    return move