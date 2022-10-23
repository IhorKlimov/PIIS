import math
from random import randrange

field_size = 5
percentage_of_walls = 0.4


class Point:
    def __init__(self, row, col, parent, finish, is_diagonal):
        self.row = row
        self.col = col
        self.parent = parent
        self.finish = finish
        self.is_diagonal = is_diagonal

    def __str__(self):
        return f"{self.row} {self.col}"

    def __repr__(self):
        return f"{self.row} {self.col}"

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.row == other.row and self.col == other.col
        return False

    def get_g_value(self):
        g = 0
        if self.parent is not None:
            g += self.parent.get_g_value()
            if self.is_diagonal:
                g += 14
            else:
                g += 10

        return g

    def get_h_value(self):
        h = 0
        h += abs(self.finish.row - self.row)
        h += abs(self.finish.col - self.col)
        return h * 10

    def get_f_value(self):
        return self.get_g_value() + self.get_h_value()

    def get_path(self):
        path = []
        current_point = self
        while current_point is not None:
            path.append(current_point)
            current_point = current_point.parent

        return list(reversed(path))


def init_coordinates(field):
    start = (randrange(field_size), randrange(field_size))
    finish = (randrange(field_size), randrange(field_size))

    while start == finish or field[start[0]][start[1]] == 0 or field[finish[0]][finish[1]] == 0:
        start = (randrange(field_size), randrange(field_size))
        finish = (randrange(field_size), randrange(field_size))

    return start, finish


def init_field():
    field = []
    for i in range(field_size):
        row = []
        for j in range(field_size):
            row.append(1)

        field.append(row)

    num_of_walls_to_add = round(field_size ** 2 * percentage_of_walls)
    walls = []
    for i in range(num_of_walls_to_add):
        walls.append((randrange(field_size), randrange(field_size)))

    for w in walls:
        r, c = w
        field[r][c] = 0

    return field


def print_field(field):
    for r in field:
        print(r)


def copy(field):
    new = []
    for r in field:
        row = []
        for c in r:
            row.append(c)

        new.append(row)

    return new


def generate_next_steps(current_point, field, history):
    steps = []

    # check left
    r, c = current_point
    if c > 0 and field[r][c - 1] != 0:
        new_field = copy(field)
        new_field[r][c - 1] = 0
        points = []
        points.extend(history)
        points.append((r, c - 1))
        steps.append((
            (r, c - 1),
            new_field,
            points
        ))

    # check right
    r, c = current_point
    if c < field_size - 1 and field[r][c + 1] != 0:
        new_field = copy(field)
        new_field[r][c + 1] = 0
        points = []
        points.extend(history)
        points.append((r, c + 1))
        steps.append((
            (r, c + 1),
            new_field,
            points
        ))

    # check top
    r, c = current_point
    if r > 0 and field[r - 1][c] != 0:
        new_field = copy(field)
        new_field[r - 1][c] = 0
        points = []
        points.extend(history)
        points.append((r - 1, c))
        steps.append((
            (r - 1, c),
            new_field,
            points
        ))

    # check down
    r, c = current_point
    if r < field_size - 1 and field[r + 1][c] != 0:
        new_field = copy(field)
        new_field[r + 1][c] = 0
        points = []
        points.extend(history)
        points.append((r + 1, c))
        steps.append((
            (r + 1, c),
            new_field,
            points
        ))

    return steps


def find_path(start, finish, field):
    states = generate_next_steps(start, field, [])
    found_path = False
    length = 0
    result = None

    while len(states) > 0:
        length += 1
        new_states = []

        for state in states:
            point, new_field, points = state
            if point == finish:
                found_path = True
                result = points
                break

            new_states.extend(generate_next_steps(point, new_field, points))

        if found_path:
            break

        states.clear()
        states.extend(new_states)

    if found_path:
        print(f"Found path! Length = {length} {result}")
    else:
        print("Didn't find a path")


def li_algorithm():
    field = init_field()
    start, finish = init_coordinates(field)
    print(f"Start {start}")
    print(f"Finish {finish}")
    field[start[0]][start[1]] = 0
    print_field(field)
    find_path(start, finish, field)


def get_neighbouring_points(point, finish, field):
    points = []
    r = point.row
    c = point.col

    # check left
    if c > 0 and field[r][c - 1] != 0:
        points.append(Point(r, c - 1, point, finish, False))

    # check right
    if c < field_size - 1 and field[r][c + 1] != 0:
        points.append(Point(r, c + 1, point, finish, False))

    # check top
    if r > 0 and field[r - 1][c] != 0:
        points.append(Point(r - 1, c, point, finish, False))

    # check down
    if r < field_size - 1 and field[r + 1][c] != 0:
        points.append(Point(r + 1, c, point, finish, False))

    # check left up
    if r > 0 and c > 0 and field[r - 1][c - 1] != 0:
        points.append(Point(r - 1, c - 1, point, finish, True))

    # check right up
    if r > 0 and c < field_size - 1 and field[r - 1][c + 1] != 0:
        points.append(Point(r - 1, c + 1, point, finish, True))

    # check left down
    if r < field_size - 1 and c > 0 and field[r + 1][c - 1] != 0:
        points.append(Point(r + 1, c - 1, point, finish, True))

    # check right down
    if r < field_size - 1 and c < field_size - 1 and field[r + 1][c + 1] != 0:
        points.append(Point(r + 1, c + 1, point, finish, True))

    return points


def pick_next_point(open_list):
    point = None

    for p in open_list:
        if point is None or p.get_f_value() < point.get_f_value():
            point = p

    return point


def a_star():
    field = init_field()
    s, f = init_coordinates(field)
    finish = Point(f[0], f[1], None, None, False)
    start = Point(s[0], s[1], None, finish, False)
    print_field(field)
    print(f"Start: {start}")
    print(f"Finish: {finish}")

    # 1
    open_list = [start]
    closed_list = []

    current_point = start

    # 2
    while True:
        if current_point == finish:
            print("Found path!")
            print(current_point.get_path())
            return

        if len(open_list) == 0:
            print("No possible path")
            return

        points = get_neighbouring_points(current_point, finish, field)
        for p in points:
            if p not in closed_list:
                # 9
                if p in open_list:
                    old = open_list[open_list.index(p)]
                    if old.get_g_value() >= p.get_g_value():
                        open_list.remove(old)
                        open_list.append(p)
                else:
                    open_list.append(p)

        # 3
        open_list.remove(current_point)
        closed_list.append(current_point)

        # 4
        current_point = pick_next_point(open_list)


def main():
    li_algorithm()
    a_star()


if __name__ == '__main__':
    main()
