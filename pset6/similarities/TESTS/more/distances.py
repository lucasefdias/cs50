from enum import Enum
import cs50


class Operation(Enum):
    """Operations"""

    DELETED = 1
    INSERTED = 2
    SUBSTITUTED = 3

    def __str__(self):
        return str(self.name.lower())


def main():

    a = cs50.get_string('a: ')
    b = cs50.get_string('b: ')

    # print(f"a = {a}")
    # print(f"b = {b}")

    distance = distances(a, b)

    # print(f"The optimal number of steps for converting {a} into {b} is {distance[len(a)][len(b)][0]}")
    # print(f"The last operation in the optimal conversion is {distance[len(a)][len(b)][1]}")
    # print()

    return 0



def distances(a, b):
    """Calculate edit distance from a to b"""

    # Setup 2d list
    matrix = []

    # print()
    # print("Before append")
    # print(matrix)

    for i in range(len(a) + 1):
        matrix.append([])

    # print("After append")
    # print(matrix)

    # Base cases
    # (0,0)
    matrix[0].append((0, None))

    # print()
    # print(f"matrix[0] = {matrix[0]}")
    # print(f"matrix[0][0] = {matrix[0][0]}")

    # First Column
    for i in range(1, len(a) + 1):
        matrix[i].append((i, Operation.DELETED))

    # First Row
    for j in range(1, len(b) + 1):
        matrix[0].append((j, Operation.INSERTED))

    # print()
    # print("After filling first row and first column")
    # print(matrix)
    # print()

    # For generic matrix[i][j]
    # print("matrix[i][j] loop")
    # print()
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            matrix[i].append(edit_distance(matrix, a, b, i, j))
            # print(f"matrix[{i}][{j}] = {matrix[i][j]}")
            # print()

    # print("Final matrix:")
    # for i in range(len(a)+1):
    #     for j in range(len(b)+1):
    #         print(matrix[i][j], end=" ")
    #     print()

    return matrix


# AUXILIAR RECURSIVE FUNCTION


def edit_distance(matrix, a, b, i, j):

    # print("INSIDE edit_distances")
    # print()

    # Calculates the costs for all possible operations

    cost_operation_list = []

    # Deletion
    deletion_cost = matrix[i - 1][j][0] + 1
    cost_operation_list.append((deletion_cost, Operation.DELETED))

    # print(f"deletion_cost = {deletion_cost}")
    # print(f"cost_operation_list = {cost_operation_list}")
    # print(f"cost_operation_list[0] = {cost_operation_list[0]}")
    # print()

    # Insertion
    insertion_cost = matrix[i][j - 1][0] + 1
    cost_operation_list.append((insertion_cost, Operation.INSERTED))

    # print(f"insertion_cost = {insertion_cost}")
    # print(f"cost_operation_list = {cost_operation_list}")
    # print(f"cost_operation_list[1] = {cost_operation_list[1]}")
    # print()

    # Substitution
    # ith character from a is the same as jth character from b (no operation needed)

    # print(f"a[{i-1}] = {a[i-1]}")
    # print(f"b[{j-1}] = {b[j-1]}")
    # print(f"a[{i-1}] == b[{j-1}]: {a[i-1] == b[j-1]}")
    # print()

    if a[i - 1] == b[j - 1]:
        substitution_cost = matrix[i - 1][j - 1][0]
    # substitution needed (one additional step)
    else:
        substitution_cost = matrix[i - 1][j - 1][0] + 1

    cost_operation_list.append((substitution_cost, Operation.SUBSTITUTED))

    # print(f"substitution_cost = {substitution_cost}")
    # print(f"cost_operation_list = {cost_operation_list}")
    # print(f"cost_operation_list[2] = {cost_operation_list[2]}")
    # print()


    # Creates a dictionary from the cost-operation tuple list
    cost_operation_dict = dict(cost_operation_list)

    # print(f"cost_operation_dict = {cost_operation_dict}")
    # print()

    # Calculates the cell cost and the corresponding operation
    cell_cost = min(deletion_cost, insertion_cost, substitution_cost)

    # print(f"cell_cost = {cell_cost}")
    # print()

    operation = cost_operation_dict[cell_cost]
    # print(f"operation = {operation}")
    # print(f"cost_operation_dict[cell_cost] = {cost_operation_dict[cell_cost]}")
    # print()

    # print(f"cost, operation = {(cell_cost, operation)}")
    # print()

    return (cell_cost, operation)


if __name__ == '__main__':
    main()