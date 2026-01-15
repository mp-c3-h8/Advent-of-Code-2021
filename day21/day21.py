import os.path
from timeit import default_timer as timer
import re
from functools import cache


def simulate(pos: int, first_roll: int) -> list[int]:
    scores = []
    score = 0
    i = 0
    for i in range(10**3):
        roll = first_roll + 18*i
        increment = roll % 10
        pos = (pos + increment)
        pos = pos % 10
        if pos == 0:
            pos = 10
        score += pos
        scores.append(score)
        if score >= 1000:
            break
    return scores


def triangle_dice(player1: int, player2: int) -> int:
    scores1 = simulate(player1, 6)
    scores2 = simulate(player2, 15)
    winning_rolls1, winning_rolls2 = len(scores1), len(scores2)
    if winning_rolls2 < winning_rolls1:  # player2 won
        rolls = winning_rolls2*2*3
        losing_points = scores1[winning_rolls2-1]
    else:  # player1 won
        rolls = (winning_rolls1*2-1)*3
        losing_points = scores2[winning_rolls1-2]
    return rolls*losing_points


@cache
def dirac_dice(pos: int, score: int, other_pos: int, other_score: int) -> tuple[int, int]:

    # number of outcomes for 3 rolls of a 3-sided die
    # sum 4: (2,1,1) or (1,2,1) or (1,1,2)
    ROLLS = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}

    p1_wins = p2_wins = 0

    for roll, num in ROLLS.items():
        new_pos = mod if (mod := (pos+roll) % 10) else 10
        new_score = score + new_pos
        if new_score >= 21:  # base case is here
            p1_wins += num
        else:
            # reverse players
            new_p2_wins, new_p1_wins = dirac_dice(other_pos, other_score, new_pos, new_score)
            p1_wins += num * new_p1_wins
            p2_wins += num * new_p2_wins

    return p1_wins, p2_wins


s = timer()


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()
start1, start2 = map(int, re.findall(r": (\d+)", data.replace("\n", "")))


p1 = triangle_dice(start1, start2)
print("Part 1:", p1)

p2 = dirac_dice(start1, 0, start2, 0)
print("Part 2:", max(p2))


e = timer()
print("time:", e - s)

print(dirac_dice.cache_info())
