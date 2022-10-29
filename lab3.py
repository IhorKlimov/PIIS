import random
from math import inf


class Board:
    def __init__(self):
        board = []
        for i in range(3):
            board.append([None, None, None])

        self.board = board
        self.turn = "X"

    def __repr__(self):
        str = ""

        for row in self.board:
            for col in row:
                str += f"{col} "

            str += "\n"

        return str

    def copy(self):
        c = Board()
        for row in range(3):
            for col in range(3):
                c.board[row][col] = self.board[row][col]

        c.turn = self.turn

        return c

    def get_possible_moves(self):
        moves = []

        for row in range(3):
            for col in range(3):
                if self.board[row][col] is None:
                    moves.append((row, col))

        return moves

    def make_move(self, point):
        self.board[point[0]][point[1]] = self.turn
        if self.turn == "X":
            self.turn = "O"
        else:
            self.turn = "X"

    def is_win(self):
        # horizontal ones
        if self.board[0][0] == self.board[0][1] == self.board[0][2] != None:
            return self.board[0][0]

        if self.board[1][0] == self.board[1][1] == self.board[1][2] != None:
            return self.board[1][0]

        if self.board[2][0] == self.board[2][1] == self.board[2][2] != None:
            return self.board[2][0]

        # vertical ones
        if self.board[0][0] == self.board[1][0] == self.board[2][0] != None:
            return self.board[0][0]

        if self.board[0][1] == self.board[1][1] == self.board[2][1] != None:
            return self.board[0][1]

        if self.board[0][2] == self.board[1][2] == self.board[2][2] != None:
            return self.board[0][2]

        # diagonal ones
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != None:
            return self.board[0][0]

        if self.board[0][2] == self.board[1][1] == self.board[2][0] != None:
            return self.board[0][2]

        all_taken = True
        for row in self.board:
            for col in row:
                if col is None:
                    all_taken = False

        if all_taken:
            return "D"

        return None


class Node:
    def __init__(self, move, side):
        self.children = []
        self.parent = None
        self.value = None
        self.move = move
        self.side = side
        if side == "X":
            self.color = 1
        else:
            self.color = -1
        self.alpha = -inf
        self.beta = inf
        self.skip = False

    def add(self, node):
        self.children.append(node)
        node.parent = self

    def __repr__(self):
        return f"{self.move}, {self.value}. Children count: {len(self.children)} {self.side}"

    def get_max_negative_negamax_value(self):
        value = None

        for n in self.children:
            if value is None or -n.value > value:
                value = -n.value

        return value

    def get_max_negative_negamax_value_with_pruning(self):
        value = None

        for n in self.children:
            if value is None or -n.value > value:
                value = -n.value
                self.alpha = max(self.alpha, value)

        return value

    def get_max_child_value(self):
        value = None

        for n in self.children:
            if value is None or n.value > value:
                value = n.value

        return value

    def get_min_child_value(self):
        value = None

        for n in self.children:
            if value is None or n.value < value:
                value = n.value

        return value

    def get_random_child_value(self):
        return self.children[random.randrange(len(self.children))].value

    def get_unrated_child(self):
        for c in self.children:
            if c.value is None and not c.skip:
                return c

        return None

    def are_all_children_rated(self):
        result = True

        for c in self.children:
            if c.value is None:
                result = False

        return result

    def get_colored_value(self):
        return self.value * self.color


def main():
    # Generate states
    board = Board()
    node = Node(None, None)
    boards = [(board, node)]

    x_wins = 0
    o_wins = 0
    drafts = 0

    while len(boards) > 0:
        new_boards = []

        for b, n in boards:
            moves = b.get_possible_moves()
            for m in moves:
                copy = b.copy()
                copy.make_move(m)

                current_node = Node(m, b.turn)

                if copy.is_win() is None:
                    new_boards.append((copy, current_node))
                elif copy.is_win() == "X":
                    # print("X Won!")
                    x_wins += 1
                    current_node.value = 1
                    current_node.value = current_node.get_colored_value()
                elif copy.is_win() == "O":
                    # print("O Won!")
                    o_wins += 1
                    current_node.value = -1
                    current_node.value = current_node.get_colored_value()
                elif copy.is_win() == "D":
                    # print("Draft")
                    drafts += 1
                    current_node.value = 0

                n.add(current_node)

        boards.clear()
        boards = new_boards

    print(f"{x_wins} {o_wins} {drafts}")
    print(node)
    print(node.children[0])
    print(node.children[0].children[0])

    # assign values, negamax
    # checked_node = node
    # while True:
    #     if checked_node is None:
    #         break
    #     if current_node.value is not None:
    #         current_node = current_node.parent
    #     if checked_node.are_all_children_rated():
    #         checked_node.value = checked_node.get_max_negative_negamax_value()
    #
    #         checked_node = checked_node.parent
    #     else:
    #         checked_node = checked_node.get_unrated_child()
    #
    # print(node.value)

    # assign values, negamax with pruning
    checked_node = node
    while True:
        if checked_node is None:
            break
        if checked_node.value is not None:
            checked_node = checked_node.parent
        if checked_node.are_all_children_rated():
            checked_node.value = checked_node.get_max_negative_negamax_value_with_pruning()
            if checked_node.parent is not None:
                checked_node.parent.alpha = max(checked_node.parent.alpha, checked_node.value)

            checked_node = checked_node.parent
        else:
            if checked_node.alpha >= checked_node.beta:
                print("Pruning")
                checked_node.skip = True
                checked_node = checked_node.get_unrated_child()
                continue

            checked_node = checked_node.get_unrated_child()
            checked_node.alpha = -checked_node.parent.alpha
            checked_node.beta = -checked_node.parent.beta

    print(node.value)




if __name__ == '__main__':
    main()
