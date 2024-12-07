INF = int(1e9)
scoreMap = {
    "5-in-row": INF,
    "4-open": 1000,
    "4-blocked": 500,
    "3-open": 200,
    "3-blocked": 50,
    "2-open": 10,
    "potential": 5
}
diffMap = {
    'easy': 2,
    'medium': 3,
    'hard': 4
}

def setDifficulty(gameDifficulty):
    return diffMap[gameDifficulty.lower()]
def isValid(grid, size, x, y):
    return (0 <= x < size and 0 <= y < size and grid[x][y] == 0)

def printGrid(grid):
    for row in grid:
        print(row, end='\n')
        
def gameOver(grid, size):
    # Check for horizontal wins
    for row in grid:
        for i in range(size - 4):
            sub = row[i:i + 5]
            if sub == [1, 1, 1, 1, 1]:
                return 1
            if sub == [2, 2, 2, 2, 2]:
                return 2

    # Check for Vertical wins
    for i in range(size):
        col = [row[i] for row in grid]
        for j in range(size - 4):
            sub = col[j:j + 5]
            if sub == [1, 1, 1, 1, 1]:
                return 1
            if sub == [2, 2, 2, 2, 2]:
                return 2
    # Check for diagonal wins
    gridReversed = [row[::-1] for row in grid]
    for i in range(size - 4):
        for j in range(size - 4):
            sub = []
            subAnti = []
            for k in range(5):
                sub.append(grid[i + k][j + k])
                subAnti.append(gridReversed[i + k][j + k])
            if sub == [1, 1, 1, 1, 1] or subAnti == [1, 1, 1, 1, 1]:
                return 1
            elif sub == [2, 2, 2, 2, 2] or subAnti == [2, 2, 2, 2, 2]:
                return 2
    for row in grid:
        if row.count(0) > 0:
            return -1
    return 0
