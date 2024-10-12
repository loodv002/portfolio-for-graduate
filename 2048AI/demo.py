from _2048board import Board
from AI_0 import AI_0
from AI_1 import AI_1
from AI_2 import AI_2
from AI_3 import AI_3

from sys import argv

if len(argv) <= 1 or not argv[1].isdigit() or not 0 <= int(argv[1]) <= 3:
    print('Usage: demp.py <model: 0-3>')
    exit(1)

# init board
board = Board()
board.add_random_number()

duration = 10

while not board.is_dead():
    if argv[1] == '0':
        way = AI_0(board.board)
    elif argv[1] == '1':
        way = AI_1(board.board)
    elif argv[1] == '2':
        way = AI_2(board.board, 3)
    elif argv[1] == '3':
        way, duration = AI_3(board.board, duration)

    changed = board.move_by_string(way)
    if changed: board.add_random_number()


    print(f'{way:>5s}, score: {board.score}, max block: {board.max_block}')
    print(board)
    print()