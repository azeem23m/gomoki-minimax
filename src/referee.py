class game_referee:

    """

        game_referee class


        Include Heuristic functions and score evaluators and game over checker
    
    """


    scoreMap = {
        "5-in-row": int(1e9),
        "4-open": 10000,
        "4-blocked": 500,
        "3-open": 400,
        "3-blocked": 50,
        "2-open": 10
    }
    diffMap = {
        'easy': 2,
        'medium': 3,
        'hard': 4
    }


    @staticmethod
    def isValidMove(grid, size, x, y):
        return (0 <= x < size and 0 <= y < size and grid[x][y] == 0)

    @staticmethod
    def center_weight(x, y, size):
        """
            This heuristic function applys some weight to cells near middle for more mid control
        """
        center = size // 2
        return size - (abs(center - x) + abs(center - y))

    @staticmethod
    def evalWindow(sub, ally, opp):

        """
            This function check for patterns and return window score
            +ve score for offensive potential, -ve for opponent threats
        """

        score = 0
        if f"{ally}{ally}{ally}{ally}{ally}" in sub:
            return game_referee.scoreMap['5-in-row']

        # Checking Offensive patterns

        if f"0{ally}{ally}{ally}{ally}0" in sub:
            score += game_referee.scoreMap['4-open']
        elif f"0{ally}{ally}{ally}0" in sub:
            score += game_referee.scoreMap['3-open']
        elif f"0{ally}{ally}0" in sub:
            score += game_referee.scoreMap['2-open']
        elif f"{ally}{ally}{ally}{ally}{opp}" in sub or f"{opp}{ally}{ally}{ally}{ally}" in sub:
            score += game_referee.scoreMap['4-blocked']
        elif f"{ally}{ally}{ally}" in sub:
            score += game_referee.scoreMap['3-blocked']

        # Checking Defensive patterns

        if f"0{opp}{opp}{opp}{opp}0" in sub:
            score -= game_referee.scoreMap['4-open']
        elif f"0{opp}{opp}{opp}0" in sub:
            score -= game_referee.scoreMap['3-open']
        elif f"0{opp}{opp}0" in sub:
            score -= game_referee.scoreMap['2-open']
        elif f"{opp}{opp}{opp}{opp}{ally}" in sub or f"{ally}{opp}{opp}{opp}{opp}" in sub:
            score += game_referee.scoreMap['4-blocked']
        elif f"{opp}{opp}{opp}" in sub:
            score += game_referee.scoreMap['3-blocked']

        return score
    @staticmethod
    def check_game_over(grid, size):

        """
            Check for game termination conditions
            returns 1 if User wins
            returns 2 if AI wins
            returns -1 if it's a tie
            returns 0 if game isn't over
        """

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
                subAntiDiag = []
                for k in range(5):
                    sub.append(grid[i + k][j + k])
                    subAntiDiag.append(gridReversed[i + k][j + k])
                if sub == [1, 1, 1, 1, 1] or subAntiDiag == [1, 1, 1, 1, 1]:
                    return 1
                elif sub == [2, 2, 2, 2, 2] or subAntiDiag == [2, 2, 2, 2, 2]:
                    return 2
        for row in grid:
            if row.count(0) > 0:
                return 0
        return -1
    @staticmethod
    def get_direction_score(grid, size, x, y, dx, dy, player):

        score = 0
        sub = ""

        for i in range(0, 6):
            newX = x + dx * i
            newY = y + dy * i
            if 0 <= newX < size and 0 <= newY < size:
                sub += str(grid[newX][newY])
        if len(sub) >= 6:
            score += game_referee.evalWindow(sub, player, 3 - player)
        return score
    @staticmethod
    def eval_grid(grid, size, isMax):

        """
            This function evaluates the board and returns a score to estimate current player advantage
            +ve score indicates player advantage -ve score means opponent advantage

            This is the main heuristic for the minimax algorithm
        """

        totalScore = 0
        player = 1 if isMax else 2
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

        for x in range(size):
            for y in range(size):
                if grid[x][y] != 0:
                    positionScore = 0
                    for dx, dy in directions:
                        directionScore = game_referee.get_direction_score(grid, size, x, y, dx, dy, player)
                        positionScore += directionScore

                    totalScore += positionScore
        return totalScore
