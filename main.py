from utils import printGrid, isValid, gameOver, setDifficulty
from ai import moveAI
def main():
    size = int(input("Grid Size: "))
    firstMove = int(input("1. AI play first\n2. You play first\n"))
    gameDifficulty = input("Game Difficulty: ")
    grid = [[0 for i in range(size)] for j in range(size)]
    isAI = True if firstMove == 1 else False
    difficulty = setDifficulty(gameDifficulty)
    END = -1

    while END == -1:
        if isAI:
            bestX, bestY = moveAI(grid, size, difficulty)
            grid[bestX][bestY] = 1
            print(f"AI moved: {bestX}, {bestY}")
            isAI = False
        else:
            printGrid(grid)
            x = int(input("Enter X: "))
            y = int(input("Enter Y: "))
            if isValid(grid, size, x, y):
                grid[x][y] = 2
                isAI = True
            else:
                print("Invalid move. Try again.")
        END = gameOver(grid, size)
    else:
        if END == 0:
            print("Tie")
        elif END == 1:
            print("You Lose")
        else:
            print("You Win")
        printGrid(grid)

if __name__ == "__main__":
    main()