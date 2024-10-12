#create_time: 0108 1537
from time import time
from typing import Tuple
from _2048board import Board

def minimax(
        board: 'Board', 
        layer: int, 
        layer_type: int, 
        alpha: float = -float('INF'), 
        beta: float = float('INF')
    ) -> Tuple[float, str, float, float]:
    '''
    implement minimax

    :param board: current Board
    :param layer: tree layer (decrease to 0 downward)
    :param layer_type: 0: moveing layer, 1: random layer
    :param alpha: max evaluation
    :param beta: min evaluation

    :return: tuple(evalution, way, alpha, beta)
    '''
    
    if (layer == 0) or board.is_dead():
        # moving layer(max)
        return board.eval(), None

    if layer_type == 0: # moving layer(max)
        ways = ['up', 'down', 'left', 'right']

        max_way = ''
        max_eval = alpha

        for way in ways:
            child = board.copy()
            changed = child.move_by_string(way)

            if not changed:
                continue

            child_eval, child_way = minimax(
                board = child, 
                layer = layer - 1,
                layer_type = 1,
                alpha = max_eval,
                beta = beta
            )

            if child_eval > max_eval:
                max_eval = child_eval
                max_way = way

            if max_eval >= beta:
                break
            
        # print(' '*((3 - layer) * 2 + (layer_type == 0)), layer_type, max_eval, beta)
        return max_eval, max_way

    elif layer_type == 1: # random layer(min)
        min_eval = beta

        for new_value in [2, 4]:
            for row, col in board.get_empty_pos():
                child = board.copy()
                child.board[row][col] = new_value

                child_eval, child_way = minimax(
                    board = child, 
                    layer = layer,
                    layer_type = 0,
                    alpha = alpha,
                    beta = min_eval
                )

                if child_eval < min_eval:
                    min_eval = child_eval

                if alpha >= min_eval:
                    break
        # print(' '*((3 - layer) * 2 + (layer_type == 0)), layer_type, alpha, min_eval)
        return min_eval, None

def AI_3(board, last_duration):
    LAYER = 3

    if last_duration < 0.05:
        LAYER = 4
    elif last_duration > 0.5:
        LAYER = 3

    board = Board(board)

    t1 = time()

    _, way = minimax(
        board = board,
        layer = LAYER,
        layer_type = 0,
    )

    t2 = time()

    return way, t2 - t1

if __name__ == '__main__':
    board = [
        [2, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    print(AI_3(board))