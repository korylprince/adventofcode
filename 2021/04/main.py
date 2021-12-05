import re

import numpy as np

class Board:
    def __init__(self, board):
        self.board = np.array(board)
        self.nums = dict()
        for row, col in np.ndindex(self.board.shape):
            self.nums[self.board[row, col]] = (row, col)
        self.marked_nums = set()
        self.last = None

    def mark(self, num):
        if num in self.nums is not None:
            self.marked_nums.add(num)
            self.last = num

    @property
    def solved(self):
        for row in self.board:
            if set(row).issubset(self.marked_nums):
                return True

        for col in self.board.T:
            if set(col).issubset(self.marked_nums):
                return True

        return False

    @property
    def score(self):
        return sum(set(self.nums.keys()).difference(self.marked_nums)) * self.last


def get_boards():
    with open("./input.txt") as f:
        boards = f.read().strip().split("\n\n")
        nums = [int(n) for n in boards[0].strip().split(",")]
        boards = [Board([[int(n) for n in re.split(r"\s+", row.strip())] for row in board.strip().splitlines()]) for board in boards[1:]]
    return nums, boards

def part1():
    nums, boards = get_boards()
    for n in nums:
        for b in boards:
            b.mark(n)
            if b.solved:
                return b

print("Answer 1:", part1().score)

def part2():
    nums, boards = get_boards()
    boards = set(boards)
    board = None
    for n in nums:
        remove = set()
        for b in boards:
            b.mark(n)
            if b.solved:
                remove.add(b)
        boards.difference_update(remove)
        if len(boards) == 1:
            board = list(boards)[0]
        if len(boards) == 0:
            return board

print("Answer 2:", part2().score)
