from random import randint, choice
from typing import List

from _2048board import Board

ROUND = 100 # decide how many times per way

def AI_0(board: List[List[int]]) -> str:
    score = {
        'up': 0, 
        'right': 0,
        'down': 0,
        'left': 0
    }
    ways = ['up', 'right', 'down', 'left']
    movable_ways = []

    for way in ways:
        new_case = Board(board)
        changed = new_case.move_by_string(way)

        if changed:
            movable_ways.append(way)

    for way in movable_ways:
        for round in range(ROUND):
            new_case = Board(board)
            new_case.move_by_string(way)
            new_case.add_random_number()

            while (not new_case.is_dead()):
                random_way = choice(ways)

                changed = new_case.move_by_string(random_way)

                if changed:
                    new_case.add_random_number()
            
            score[way] += new_case.score

    # print(score)

    max_key = movable_ways[0]

    for key, value in score.items():
        if value > score[max_key]:
            max_key = key

    return max_key


if __name__ == '__main__':
    board = [
        [2, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    print(AI_0(board))