import time
from referee import game_referee


class AI:

    """
        AI class

        Implementation of Minimax algorithm with alpha beta pruning

    """

    @staticmethod
    def make_move(grid, size, depth):

        start_time = time.time()
        _, move = AI.minimax(grid, size, depth, True)
        print(f"AI Moved: {move}\nTime to make move: {time.time() - start_time}")
        return move

    @staticmethod
    def minimax(grid, size, depth, isMax, alpha=-int(1e9), beta=int(1e9)):
        
        result = game_referee.check_game_over(grid, size)
        if depth == 0 or result:
            if result == 1:
                return int(1e9), None
            if result == 2:
                return -int(1e9), None
            if result == -1:
                return 0, None

            return game_referee.eval_grid(grid, size, isMax), None

        bestMove = [-1, -1]
        if isMax:
            maxScore = -int(1e9)
            for i in range(size):
                for j in range(size):
                    if grid[i][j] == 0:
                        grid[i][j] = 1
                        score, _ = AI.minimax(grid, size, depth - 1, False, alpha, beta)
                        score += game_referee.center_weight(i, j, size)
                        grid[i][j] = 0
                        if score > maxScore:
                            maxScore = score
                            bestMove = [i, j]
                        alpha = max(alpha, score)
                        if beta <= alpha:
                            break
            return maxScore, bestMove

        else:
            minScore = int(1e9)
            for i in range(size):
                for j in range(size):
                    if grid[i][j] == 0:
                        grid[i][j] = 2
                        score, _ = AI.minimax(grid, size, depth - 1, True, alpha, beta)
                        score -= game_referee.center_weight(i, j, size)
                        grid[i][j] = 0
                        if score < minScore:
                            minScore = score
                            bestMove = [i, j]
                        beta = min(beta, score)
                        if beta <= alpha:
                            break

            return minScore, bestMove


