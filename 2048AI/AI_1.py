# update_time: 0114 1033
from random import randint, choice
from typing import List
from time import time

from _2048board import Board

TIME_LIMIT = 0.237 # decide how many times per step

def AI_1(board: List[List[int]]) -> str:
    score = {
        'up': 0, 
        'right': 0,
        'down': 0,
        'left': 0
    }
    run_time = {
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
        start_time = time()

        while (time() - start_time < TIME_LIMIT / len(movable_ways)):
            new_case = Board(board)
            new_case.move_by_string(way)
            new_case.add_random_number()

            while (not new_case.is_dead()):
                random_way = choice(ways)

                changed = new_case.move_by_string(random_way)

                if changed:
                    new_case.add_random_number()
            
            score[way] += new_case.score
            run_time[way] += 1

    for key in score.keys():
        if run_time[key]:
            score[key] /= run_time[key]

    '''
    print(score)
    print(run_time)
    #'''

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

    print(AI_1(board))