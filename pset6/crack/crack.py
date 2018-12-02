# ----------------------------------------------
# CS50 Problem Set 6: Sentimental - Crack
#
# Summary: Reimplements Crack in Python
# Cracks a hashed password provided by the user
#
# Lucas Emidio Fernandes Dias
# 17 October 2018
# ----------------------------------------------

# Import modules
import crypt
import itertools
import string
import sys

# Constant - password maximum size
PWD_MAX = 6

# --------------------
#  MAIN
# --------------------


def main():

    # Error handling
    if len(sys.argv) < 2:
        print("Error: Missing an argument")
        print("Usage: python crack.py hash")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("Error: Too many arguments")
        print("Usage: python crack.py hash")
        sys.exit(1)
    # len(argv) = 2: Run normal procedures
    else:

        # Get hash and salt from argv[1]
        password_hash = sys.argv[1]
        salt = password_hash[:2]

        # Iterate over key possibilities until password is cracked (all permutations up to 5 chars)
        # Passwords are permutations of uppercase and lowercase letters
        iterable_chars = string.ascii_letters

        for pwd_size in range(1, PWD_MAX):

            if iterate_passwords(password_hash, salt, pwd_size, iterable_chars):
                sys.exit(0)

        # If loop is over, password was not found
        print("Error: password could not be cracked")
        sys.exit(1)


# ------------------
# Auxiliar functions
# ------------------


def iterate_passwords(password_hash, salt, pwd_size, iterable_chars):
    """ Checks all possibilities of alphabetical characters password for a
    given password size and returns True if password is found """

    keys = map("".join, itertools.product(iterable_chars, repeat=pwd_size))

    for key in keys:

        # Check if password was found and print the password if found
        if crypt.crypt(key, salt) == password_hash:
            print(key)
            return True

    return False


if __name__ == '__main__':
    main()