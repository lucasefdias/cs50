from enum import Enum


class Operation(Enum):
    """Operations"""

    DELETED = 1
    INSERTED = 2
    SUBSTITUTED = 3

    def __str__(self):
        return str(self.name.lower())


def distances(a, b):
    """Calculate edit distance from a to b"""

    # Setup 2d list
    matrix = []
    for i in range(len(a) + 1):
        matrix.append([])

    # Base cases
    # (0,0)
    matrix[0].append((0, None))

    # First Column
    for i in range(1, len(a) + 1):
        matrix[i].append((i, Operation.DELETED))

    # First Row
    for j in range(1, len(b) + 1):
        matrix[0].append((j, Operation.INSERTED))

    # For generic matrix[i][j]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            matrix[i].append(edit_distance(matrix, a, b, i, j))

    return matrix


# AUXILIAR RECURSIVE FUNCTION


def edit_distance(matrix, a, b, i, j):
    """ Calculates the costs for all possible operations and
        returns minimum cost and corresponding operation """

    cost_operation_list = []

    # Deletion
    deletion_cost = matrix[i - 1][j][0] + 1
    cost_operation_list.append((deletion_cost, Operation.DELETED))

    # Insertion
    insertion_cost = matrix[i][j - 1][0] + 1
    cost_operation_list.append((insertion_cost, Operation.INSERTED))

    # Substitution
    # ith character from a is the same as jth character from b (no operation needed)
    if a[i - 1] == b[j - 1]:
        substitution_cost = matrix[i - 1][j - 1][0]
    # substitution needed (one additional step)
    else:
        substitution_cost = matrix[i - 1][j - 1][0] + 1

    cost_operation_list.append((substitution_cost, Operation.SUBSTITUTED))

    # Creates a dictionary from the cost-operation tuple list
    cost_operation_dict = dict(cost_operation_list)

    # Calculates the cell cost and the corresponding operation
    cost = min(deletion_cost, insertion_cost, substitution_cost)

    operation = cost_operation_dict[cost]

    return (cost, operation)