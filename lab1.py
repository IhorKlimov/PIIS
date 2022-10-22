from random import randrange

field_size = 5
percentage_of_walls = 0.4


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


def main():
    field = init_field()
    start, finish = init_coordinates(field)

    print(f"Start {start}")
    print(f"Finish {finish}")

    field[start[0]][start[1]] = 0
    print_field(field)

    find_path(start, finish, field)


if __name__ == '__main__':
    main()
