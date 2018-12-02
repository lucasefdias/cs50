# ----------------------------------------------
# CS50 Problem Set 6: Sentimental - Mario (more)
#
# Summary: Reimplements Mario (more) in python
# Prints Mario`s pyramid (more)
#
# Lucas Emidio Fernandes Dias
# 03 October 2018
# ----------------------------------------------

from cs50 import get_int

# Constants
# Gap width
GAP = 2

# Asks the user for a height until height is valid
while True:

    height = get_int("Height: ")

    # Height is only valid if 0 <= height <= 23
    if height >= 0 and height <= 23:
        break

# Prints the pyramid
for i in range(height):

    # Print left pyramid
    # Print spaces
    print(" " * (height - 1 - i), end="")

    # Print hashes
    print("#" * (i + 1), end="")

    # Print gap
    print(" " * GAP, end="")

    # Print right pyramid
    # Print hashes
    print("#" * (i + 1), end="")

    # Print new line
    print("")