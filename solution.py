from collections import Counter

assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'


def cross(first, second):
    return [x + y for x in first for y in second]


boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

# Diagonal units
main_diag = [a + b for a, b in zip(rows, cols)]
anti_diag = [a + b for a, b in zip(rows, cols[::-1])]
diag_units = [main_diag, anti_diag]

unit_list = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unit_list if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - {s}) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    if values[box] == value:
        return values

    values[box] = value

    if len(value) == 1:
        assignments.append(values.copy())

    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unit_list:
        # Find values of length 2 in a unit which appear more than once
        duplicates = [val for val, count in
                      Counter([values[box] for box in unit if len(values[box]) == 2]).items()
                      if count > 1]

        for dup in duplicates:
            for box in unit:
                # Don't touch the duplicate itself
                if values[box] == dup:
                    continue

                for digit in dup:
                    assign_value(values, box, values[box].replace(digit, ''))

    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) == 81
    return dict(zip(boxes, [char if char != '.' else '123456789' for char in grid]))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)

    for row in rows:
        print(''.join(values[row + col].center(width) + ('|' if col in '36' else '') for col in cols))
        if row in 'CF':
            print(line)


def eliminate(values):
    """
    :rtype: dict
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]

    for box in solved_values:
        digit = values[box]

        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(digit, ''))

    return values


def only_choice(values):
    """
    :rtype: dict
    """
    for unit in unit_list:
        for digit in '123456789':
            digit_boxes = [box for box in unit if digit in values[box]]

            if len(digit_boxes) == 1:
                assign_value(values, digit_boxes[0], digit)

    return values


def reduce_puzzle(values):
    stalled = False

    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        values = naked_twins(values)
        values = eliminate(values)
        values = only_choice(values)

        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])

        stalled = solved_values_before == solved_values_after

        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return values


def search(values):
    values = reduce_puzzle(values)

    if values is False:
        return False

    if all(len(values[box]) == 1 for box in boxes):
        return values

    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    for value in values[s]:
        new_values = values.copy()
        new_values[s] = value

        attempt = search(new_values)

        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
