# ----------------------------------------------
# CS50 Problem Set 6: Sentimental - Caesar
#
# Summary: Reimplements Caesar in Python
# Encrypts input messages using Caesar's cipher
# with a key input (k) from user
#
# Lucas Emidio Fernandes Dias
# 09 October 2018
# ----------------------------------------------

# Import modules
import sys
import cs50

# Constants
ALPHABET_LETTERS = 26


def main():

    # Error handling
    if len(sys.argv) < 2:
        print("Error: Missing an argument")
        print("Usage: python caesar.py k")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("Error: Too many arguments")
        print("Usage: python caesar.py k")
        sys.exit(1)
    # len(argv) = 2: Run normal procedures
    else:

        # Get user input from command line
        k = int(sys.argv[1])

        # Get plaintext
        print("plaintext: ", end="")
        p = cs50.get_string()

        # Encipher and then print ciphertext
        print("ciphertext: ", end="")

        # Iterate over characters of plaintext and cipher each one
        for c in p:

            # If c is an alphabetic character, shift by key (encipher)
            if c.isalpha():
                c = encipher(c, k)

            print(c, end="")

        print()

        sys.exit(0)


# Auxiliar functions


def encipher(c, k):
    """ Enciphers alphabetical characters """

    # Get corresponding ASCII integer of character
    c_integer = ord(c)

    # Convert ASCII index to alphabetical index
    c_integer = ascii_to_alpha(c, c_integer)

    # Shift plaintext character by key
    c_integer = (c_integer + k) % ALPHABET_LETTERS

    # Convert alphabetical index to ASCII index
    c_integer = alpha_to_ascii(c, c_integer)

    # Get corresponding character of ASCII index
    c = chr(c_integer)

    return c


def ascii_to_alpha(c, c_integer):
    """ Converts ASCII index to alphabetical index """

    # For uppercase
    if c.isupper():
        c_integer -= ord('A')
    # For lowercase
    else:
        c_integer -= ord('a')

    return c_integer


def alpha_to_ascii(c, c_integer):
    """ Converts alphabetical index to ASCII index """

    # For uppercase
    if c.isupper():
        c_integer += ord('A')
    # For lowercase
    else:
        c_integer += ord('a')

    return c_integer


if __name__ == '__main__':
    main()