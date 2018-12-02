import cs50
import sys

def main():

    a = sys.argv[1]
    b = sys.argv[2]

     # Read files
    try:
        with open(a, "r") as file:
            file1 = file.read()
    except IOError:
        sys.exit(f"Could not read {a}")
    try:
        with open(b, "r") as file:
            file2 = file.read()
    except IOError:
        sys.exit(f"Could not read {b}")

    same_lines = lines(file1, file2)

    # print("Same lines: ")
    # for line in same_lines:
    #     print(line)

    sys.exit(0)


def lines(a, b):

    """Return lines in both a and b"""

    # print("a:")
    # print(a)
    # print("b:")
    # print(b)

    # Splits lines from a and b into two lists
    a_lines = a.splitlines()
    b_lines = b.splitlines()

    # print("a_list:")
    # print(a_list)
    # print("b_list:")
    # print(b_list)

    # Convert lists into sets to eliminate duplicates
    a_lines = set(a_lines)
    b_lines = set(b_lines)

    # print("a_set:")
    # print(a_set)
    # print("b_set:")
    # print(b_set)

    # Finds the intersection between the two sets (lines in both a and b)
    intersect = a_lines.intersection(b_lines)

    # print("Intersect:")
    # print(intersect)

    # Creates list for common lines and appends all elements from intersection
    common_lines = []

    for element in intersect:
        common_lines.append(element)

    # for line in common_lines:
    #     print(line)

    return common_lines


if __name__ == '__main__':
    main()