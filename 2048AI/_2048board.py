from random import randint, choice
from typing import List, Optional
from math import log
from copy import deepcopy

class Board:
    def __init__(self, board: Optional[List[List[int]]] = None, score: int = 0, max_block: int = 2):
        if board:
            self.board = deepcopy(board)
        else:
            self.board = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]

        self.score = score
        self.max_block = max_block

    def __str__(self):
        return '\n'.join(' '.join(f'{col:6d}' for col in row) for row in self.board)

    def copy(self) -> 'Board':
        return Board(
            self.board, 
            self.score, 
            self.max_block
        )

    def get_empty_pos(self) -> List[List[int]]:
        empty = []

        for row in range(4):
            for col in range(4):
                if self.board[row][col] == 0:
                    empty.append((row, col))

        return empty


    def is_dead(self) -> bool:
        # alive if 0 in board 
        for row in range(4):
            for col in range(4):
                if self.board[row][col] == 0:
                    return False

        # alive if two neighbor elements of a row are the same
        for row in range(4):
            for col in range(3):
                if self.board[row][col] == self.board[row][col + 1]:
                    return False

        # alive if two neighbor elements of a column are the same
        for col in range(4):
            for row in range(3):
                if self.board[row][col] == self.board[row + 1][col]:
                    return False
        
        return True

    def add_random_number(self):
        if self.is_dead():
            return

        # decide new block value (2 or 4)
        if randint(0, 9):
            new_block_value = 2
        else:
            new_block_value = 4

        # find empty positions
        empty_pos = self.get_empty_pos()

        row, col = choice(empty_pos)

        # fill value into empty position
        self.board[row][col] = new_block_value
        
        return

    def move_upward(self) -> bool:
        changed = False

        for col in range(4):
            uncombined_row = 0

            while uncombined_row < 3:
                next_row = uncombined_row + 1

                while next_row < 4: # find next non-zero block
                    if self.board[next_row][col] == 0:
                        next_row += 1
                    else:
                        break

                if next_row == 4: # no other non-zero block
                    break

                if self.board[uncombined_row][col] == 0: # move to empty space
                    self.board[uncombined_row][col] = self.board[next_row][col]
                    self.board[next_row][col] = 0
                    changed = True

                elif self.board[uncombined_row][col] == self.board[next_row][col]: # combine blocks
                    self.board[uncombined_row][col] = self.board[uncombined_row][col] * 2
                    self.board[next_row][col] = 0

                    self.score += self.board[uncombined_row][col]
                    self.max_block = max(self.max_block, self.board[uncombined_row][col])

                    uncombined_row += 1
                    changed = True

                elif self.board[uncombined_row][col] != self.board[next_row][col]: # can not combine, move later if needed
                    uncombined_row += 1
        
        return changed

    def move_downward(self) -> bool:
        changed = False

        for col in range(4):
            uncombined_row = 3

            while uncombined_row >= 0:
                next_row = uncombined_row - 1

                while next_row >= 0:
                    if self.board[next_row][col] == 0:
                        next_row -= 1
                    else:
                        break

                if next_row == -1:
                    break

                if self.board[uncombined_row][col] == 0:
                    self.board[uncombined_row][col] = self.board[next_row][col]
                    self.board[next_row][col] = 0
                    changed = True

                elif self.board[uncombined_row][col] == self.board[next_row][col]:
                    self.board[uncombined_row][col] = self.board[uncombined_row][col] * 2
                    self.board[next_row][col] = 0

                    self.score += self.board[uncombined_row][col]
                    self.max_block = max(self.max_block, self.board[uncombined_row][col])
                    
                    uncombined_row -= 1
                    changed = True

                elif self.board[uncombined_row][col] != self.board[next_row][col]:
                    uncombined_row -= 1
        
        return changed

    def move_leftward(self) -> bool:
        changed = False

        for row in range(4):
            uncombined_col = 0

            while uncombined_col < 3:
                next_col = uncombined_col + 1

                while next_col < 4:
                    if self.board[row][next_col] == 0:
                        next_col += 1
                    else:
                        break

                if next_col == 4:
                    break

                if self.board[row][uncombined_col] == 0:
                    self.board[row][uncombined_col] = self.board[row][next_col]
                    self.board[row][next_col] = 0
                    changed = True

                elif self.board[row][uncombined_col] == self.board[row][next_col]:
                    self.board[row][uncombined_col] = self.board[row][uncombined_col] * 2
                    self.board[row][next_col] = 0

                    self.score += self.board[row][uncombined_col]
                    self.max_block = max(self.max_block, self.board[row][uncombined_col])

                    uncombined_col += 1
                    changed = True

                elif self.board[row][uncombined_col] != self.board[row][next_col]:
                    uncombined_col += 1
        
        return changed

    def move_rightward(self) -> bool:
        changed = False

        for row in range(4):
            uncombined_col = 3

            while uncombined_col >= 0:
                next_col = uncombined_col - 1

                while next_col >= 0:
                    if self.board[row][next_col] == 0:
                        next_col -= 1
                    else:
                        break

                if next_col == -1:
                    break

                if self.board[row][uncombined_col] == 0:
                    self.board[row][uncombined_col] = self.board[row][next_col]
                    self.board[row][next_col] = 0
                    changed = True

                elif self.board[row][uncombined_col] == self.board[row][next_col]:
                    self.board[row][uncombined_col] = self.board[row][uncombined_col] * 2
                    self.board[row][next_col] = 0

                    self.score += self.board[row][uncombined_col]
                    self.max_block = max(self.max_block, self.board[row][uncombined_col])

                    uncombined_col -= 1
                    changed = True

                elif self.board[row][uncombined_col] != self.board[row][next_col]:
                    uncombined_col -= 1
        
        return changed

    def move_by_string(self, way) -> bool:
        if way == 'up':
            return self.move_upward()
        elif way == 'right':
            return self.move_rightward()
        elif way == 'down':
            return self.move_downward()
        elif way == 'left':
            return self.move_leftward()

        return False

    def move_by_int(self, way) -> bool:
        '''
        :way:
           0
           |
        3--+--1
           |
           2
        '''
        if way == 0:
            return self.move_upward()
        elif way == 1:
            return self.move_rightward()
        elif way == 2:
            return self.move_downward()
        elif way == 3:
            return self.move_leftward()

        return False

    def eval(self) -> float: # for AI_2: evaluate heristic
        SMOOTH_WEIGHT = 0.1
        MONO_WEIGHT = 1.0
        EMPTY_WEIGHT = 2.7
        MAX_WEIGHT = 1.0

        return (
            self.smoothness() * SMOOTH_WEIGHT +
            self.monotonicity() * MONO_WEIGHT + 
            log(self.emptyblocks() + 1e-100) * EMPTY_WEIGHT +
            log(self.max_block, 2) * MAX_WEIGHT
        )

    def smoothness(self) -> float: # for AI_2
        smooth = 0

        for row in range(4):
            for col in range(4):
                if self.board[row][col] != 0:
                    cur_2base = log(self.board[row][col], 2)
                    
                    # check smoothness between current block and block downward 
                    next_row = row + 1

                    while next_row < 4 and self.board[next_row][col] == 0:
                        next_row += 1
                    
                    if next_row < 4 and self.board[next_row][col] != 0:
                        next_2base = log(self.board[next_row][col], 2)
                        smooth -= abs(cur_2base - next_2base)

                    # check smoothness between current block and block rightward 
                    next_col = col + 1

                    while next_col < 4 and self.board[row][next_col] == 0:
                        next_col += 1
                    
                    if next_col < 4 and self.board[row][next_col] != 0:
                        next_2base = log(self.board[row][next_col], 2)
                        smooth -= abs(cur_2base - next_2base)

        return smooth

    def monotonicity(self) -> float: # for AI_2
        left = right = up = down = 0 # decrease count

        # check left-right direction
        for row in range(4):
            no_zero_row = [ self.board[row][col] for col in range(4) if self.board[row][col] ]

            left_col = 0
            right_col = 1

            while right_col < len(no_zero_row):
                left_2base = log(no_zero_row[left_col], 2)
                right_2base = log(no_zero_row[right_col], 2)

                if left_2base > right_2base:
                    right += right_2base - left_2base
                elif left_2base < right_2base:
                    left += left_2base - right_2base

                left_col += 1
                right_col += 1

        # check up-down direction
        for col in range(4):
            no_zero_col = [ self.board[row][col] for row in range(4) if self.board[row][col] ]

            up_row = 0
            down_row = 1

            while down_row < len(no_zero_col):
                up_2base = log(no_zero_col[up_row], 2)
                down_2base = log(no_zero_col[down_row], 2)

                if up_2base > down_2base:
                    down += down_2base - up_2base
                elif up_2base < down_2base:
                    up += up_2base - down_2base

                up_row += 1
                down_row += 1
                
        return max(left, right) + max(up, down)
    
    def emptyblocks(self) -> int: # for AI_2
        return len(self.get_empty_pos())