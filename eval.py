from utils import scoreMap

def evalWindow(sub, ally, opp):
    countAlly = sub.count(ally)
    countOpp = sub.count(opp)
    countEmpty = sub.count(0)
    score = 0
    if countAlly == 5:
        return scoreMap['5-in-row']
    # Offensive patterns
    if countOpp == 0:
        if countAlly == 4:
            score += scoreMap['4-open']
        elif countAlly == 3:
            score += scoreMap['3-open']
        elif countAlly == 2:
            score += scoreMap['2-open']
    elif countOpp == 1:
        if countAlly == 4:
            score += scoreMap['4-blocked']
        elif countAlly == 3:
            score += scoreMap['3-blocked']

    # Defensive patterns
    if countAlly == 0:
        if countOpp == 4:
            if countEmpty == 1:
                score -= scoreMap['4-open']
            else:
                score -= scoreMap['4-blocked']
        elif countOpp == 3 and countEmpty >= 1:
            if countEmpty == 2:
                score -= scoreMap['3-open']
            else:
                score -= scoreMap['3-blocked']
    return score


def getDirectionScore(grid, size, x, y, dx, dy, player):
    score = 0
    sub = []

    for i in range(-4, 5):
        newX = x + dx * i
        newY = y + dy * i
        if 0 <= newX < size and 0 <= newY < size:
            sub.append(grid[newX][newY])
    if len(sub) >= 5:
        max_score = 0
        for i in range(len(sub) - 4):
            curr_score = evalWindow(sub[i:i + 5], player, 3 - player)
            if abs(curr_score) > abs(max_score):
                max_score = curr_score
        score += max_score
    return score

def evaluatePosition(grid, size, isMax):
    totalScore = 0
    player = 1 if isMax else 2
    directions = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    for x in range(size):
        for y in range(size):
            if grid[x][y] != 0:
                positionScore = 0
                # Evaluate patterns in all directions
                for dx, dy in directions:
                    directionScore = getDirectionScore(grid, size, x, y, dx, dy, player)
                    positionScore += directionScore

                totalScore += positionScore
    return totalScore