import os.path
import re
from collections import defaultdict


type Pos = tuple[int, int]  # (y,x)
type BoardPos = tuple[Board, Pos]
type BoardMatrix = list[list[int]]


class Board:
    # numbers found on corresponding boards for fast lookup
    board_positions: defaultdict[int, set[BoardPos]] = defaultdict(set)

    def __init__(self, board_str: str) -> None:
        self.numbers: BoardMatrix = [[*map(int, re.findall(r"\d+", row))] for row in board_str.splitlines()]
        self.marked_numbers: BoardMatrix = [[0]*len(self.numbers[0]) for _ in range(len(self.numbers))]  # mask
        self.size: int = len(self.numbers)
        self.last_number: int | None = None
        self.last_pos: Pos | None = None
        for y, row in enumerate(self.numbers):
            for x, n in enumerate(row):
                self.__class__.add_board_position(self, n, (y, x))

    def mark(self, pos: Pos, n: int) -> None:
        y, x = pos
        self.marked_numbers[y][x] = 1
        self.last_number = n
        self.last_pos = pos
        return

    def is_winning(self) -> bool:
        if self.last_pos is None:
            return False
        y, x = self.last_pos
        return (
            all(m == 1 for m in self.marked_numbers[y]) or
            all(self.marked_numbers[i][x] == 1 for i in range(self.size))
        )

    def score(self) -> int:
        if self.last_number is None:
            return 0
        sum_unmarked = sum(
            sum(n for n, m in zip(r1, r2) if m == 0)
            for r1, r2 in zip(self.numbers, self.marked_numbers)
        )
        return sum_unmarked * self.last_number

    @classmethod
    def add_board_position(cls, board: Board, n: int, pos: Pos) -> None:
        cls.board_positions[n].add((board, pos))

    def __repr__(self) -> str:
        return f"numbers: {self.numbers}, marked: {self.marked_numbers}"


def bingo(draw_str: str) -> list[int]:
    winners: set[Board] = set()
    scores: list[int] = []
    for num_str in draw_str.split(","):
        n = int(num_str)
        scores_this_draw: list[int] = []
        for board, pos in Board.board_positions[n]:
            if board in winners:
                continue
            board.mark(pos, n)
            if board.is_winning():
                scores_this_draw.append(board.score())
                winners.add(board)
        if scores_this_draw:
            scores.extend(sorted(scores_this_draw, reverse=True))
    return scores


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

drawn_str, *boards_str = data.split("\n\n")

boards: list[Board] = [Board(board_str) for board_str in boards_str]
winning_scores = bingo(drawn_str)

print("Part 1:", winning_scores[0])
print("Part 2:", winning_scores[-1])
