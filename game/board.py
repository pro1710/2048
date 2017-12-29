from copy import deepcopy


class Move:
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'

    VUP = (-1, 0)
    VDOWN = (1, 0)
    VLEFT = (0, -1)
    VRIGHT = (0, 1)

    VMOVES = {UP: VUP, DOWN: VDOWN, LEFT: VLEFT, RIGHT: VRIGHT}

    NONE = 'NONE'
    EXIT = 'EXIT'


class Board:
    DEFAULT_BOARD_SIZE = 4

    def __init__(self, board_size=DEFAULT_BOARD_SIZE):
        self.__board_size = board_size
        self.__board = [[0] * self.__board_size for _ in range(self.__board_size)]

    def __len__(self):
        return len(self.__board)

    @property
    def board(self):
        return self.__board

    @property
    def size(self):
        return self.__board_size

    def clone(self):
        return deepcopy(self)

    def clear(self):
        for i in range(self.__board_size):
            for j in range(self.__board_size):
                self.__board[i][j] = 0

    def init(self):
        self.clear()

    def set_cell_value(self, pos, value=0):
        self.__board[pos[0]][pos[1]] = value

    def get_cell_value(self, pos):
        if 0 > pos[0] or 0 > pos[1]:
            raise IndexError

        return self.__board[pos[0]][pos[1]]

    def board_columns(self):
        return [[self.get_cell_value((j, i)) for j in range(self.__board_size)] for i in range(self.__board_size)]

    def get_empty_cells(self):
        empty_cells = []
        for i in range(self.__board_size):
            for j in range(self.__board_size):
                if not self.get_cell_value((i, j)):
                    empty_cells.append((i, j))
        return empty_cells

    def display(self):
        pattern = '{:=5}' * self.__board_size
        print('\n'.join([pattern.format(*line) for line in self.__board]))

    def score(self):
        return max([max(line) for line in self.__board])

    def can_move(self, direction=Move.VMOVES):
        moves2check = set(direction)
        for i in range(self.__board_size):
            for j in range(self.__board_size):
                if self.__board[i][j] == 0:
                    return True

                else:
                    for move in moves2check:
                        vmove = Move.VMOVES[move]
                        try:
                            adj_cell = self.get_cell_value((i + vmove[0], j + vmove[1]))
                            if adj_cell == self.get_cell_value((i, j)) or adj_cell == 0:
                                return True
                        except IndexError:
                            continue
        return False

    def make_move(self, direction):
        # TODO: refactor
        def merge(lst):
            non_zero = [val for val in lst if val]
            i = 0
            while i < len(non_zero) - 1:
                if non_zero[i] == non_zero[i + 1]:
                    non_zero[i] *= 2
                    del non_zero[i + 1]
                i += 1
            return non_zero + [0] * (self.__board_size - len(non_zero))

        result = False
        if direction == Move.UP:
            for col_idx, col in enumerate(self.board_columns()):
                merged = merge(col)

                if merged == col:
                    continue

                for line_idx in range(self.__board_size):
                    # print('set: (%d, %d) = %d'% (line_idx, col_idx, merged[line_idx]))
                    self.set_cell_value((line_idx, col_idx), merged[line_idx])
                result = True

        elif direction == Move.DOWN:
            for col_idx, col in enumerate(self.board_columns()):
                merged = merge(reversed(col))
                merged.reverse()

                if merged == col:
                    continue

                for line_idx in range(self.__board_size):
                    # print('set: (%d, %d) = %d'% (line_idx, col_idx, merged[line_idx]))
                    self.set_cell_value((line_idx, col_idx), merged[line_idx])
                result = True

        elif direction == Move.LEFT:
            for line_idx, line in enumerate(self.__board):
                merged = merge(line)

                if merged == line:
                    continue

                for col_idx in range(self.__board_size):
                    # print('set: (%d, %d) = %d' % (line_idx, col_idx, merged[col_idx]))
                    self.set_cell_value((line_idx, col_idx), merged[col_idx])
                result = True

        elif direction == Move.RIGHT:
            for line_idx, line in enumerate(self.__board):
                merged = merge(reversed(line))
                merged.reverse()

                if merged == line:
                    continue

                for col_idx in range(self.__board_size):
                    # print('set: (%d, %d) = %d' % (line_idx, col_idx, merged[col_idx]))
                    self.set_cell_value((line_idx, col_idx), merged[col_idx])
                result = True

        return result

