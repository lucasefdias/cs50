# ----------------------------------------------
# CS50 Problem Set 6: Sentimental - Vigenère
#
# Summary: Reimplements Caesar in Python
# Encrypts input messages using Vigenère's cipher
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

# --------------------
#  MAIN
# --------------------


def main():

    # Error handling
    if len(sys.argv) < 2:
        print("Error: Missing an argument")
        print("Usage: python vigenere.py k")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("Error: Too many arguments")
        print("Usage: python vigenere.py k")
        sys.exit(1)
    # len(argv) = 2: Run normal procedures
    else:

        # Check if argv[1] contains only alphabetical characters
        if not sys.argv[1].isalpha():
            print("Error: Argument must contain only alphabetical characters")
            print("Usage: python vigenere.py k")
            sys.exit(1)

        # Convert argv[1] string to list of integers (k) using alphabetical index
        i = 0
        k = []
        for c in sys.argv[1]:
            k.append(ord(c))
            print(f"k[{i}] = {k[i]}")

            k[i] = ascii_to_alpha(c, k[i])
            print(f"k[{i}] = {k[i]}")

            i += 1

        # Get plaintext
        print("plaintext: ", end="")
        p = cs50.get_string()

        # Encipher and then print ciphertext
        print("ciphertext: ", end="")

        # Loop through every character in plaintext (p) and cipher it using k
        # j: k counter; k_length: length of list k
        j = 0
        k_length = len(k)
        for c in p:

            # If c is an alphabetic character, shift by key (encipher)
            if c.isalpha():
                c = encipher(c, k[j])
                j = (j + 1) % k_length

            print(c, end="")

        print()

        sys.exit(0)


# ------------------
# Auxiliar functions
# ------------------


def encipher(c, k):
    """Enciphers alphabetical characters """

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