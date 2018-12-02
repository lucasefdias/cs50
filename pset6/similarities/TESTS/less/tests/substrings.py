import cs50
import sys

def main():

    a = sys.argv[1]
    b = sys.argv[2]
    n = int(sys.argv[3])

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

    same_substrings = substrings(file1, file2, n)

    # print("Same lines: ")
    # for line in same_lines:
    #     print(line)

    sys.exit(0)


def substrings(a, b, n):

    """Return substrings of length n in both a and b"""

    print("a:")
    print(a)
    print("b:")
    print(b)

    # Splits sentences from a and b into two lists
    a_substrings = get_substrings(a, n)
    b_substrings = get_substrings(b, n)

    print("a_substrings:")
    print(a_substrings)
    print("b_substrings:")
    print(b_substrings)

    # Convert lists into sets to eliminate duplicates
    a_substrings = set(a_substrings)
    b_substrings = set(b_substrings)

    print("a_substrings:")
    print(a_substrings)
    print("b_substrings:")
    print(b_substrings)

    # Finds the intersection between the two sets (sentences in both a and b)
    intersect = a_substrings.intersection(b_substrings)

    print("Intersect:")
    print(intersect)

    # Creates list for common sentences and appends all elements from intersection
    common_substrings = []

    for element in intersect:
        common_substrings.append(element)

    for substring in common_substrings:
        print(substring)

    return common_substrings


def get_substrings(string, n):

    substring_list = []

    for i in range(len(string) - n):
        substring_list.append(string[i:i+n])

    return substring_list


if __name__ == '__main__':
    main()
