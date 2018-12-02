# ----------------------------------------------
# CS50 Problem Set 6: Sentimental - Credit
#
# Summary: Reimplements Credit in Python
# Asks the user for an input (number) and
# evaluates if the input is a valid credit
# card number
#
# Lucas Emidio Fernandes Dias
# 08 October 2018
# ----------------------------------------------

import cs50

# Prompts the user for credit card number
while True:

    cc_number = cs50.get_int("Number: ")

    if cc_number >= 0:
        break

# Create a string from credit card number
cc_number_str = str(cc_number)

# Credit card number length for number validation
cc_number_length = len(cc_number_str)

# Checksum procedure
# Initializes checksum and position counter
checksum = 0
position = 0

# Loops through all digits from cc_number, from position 0 (last digit) until first digit
while cc_number > 0:

    position += 1

    # Get current digit
    digit = cc_number % 10
    cc_number //= 10

    # Every other digit procedure
    if position % 2 == 0:

        digit *= 2

        if digit >= 10:
            checksum += digit % 10 + digit // 10
        else:
            checksum += digit

    # Remaining digits procedure
    else:
        checksum += digit

# If checksum is valid, evalutes id. Else, card number is invalid
if checksum % 10 == 0:

    # Checks for AMEX id
    amex = True if cc_number_length == 15 and (cc_number_str[:2] == "34" or cc_number_str[:2] == "37") else False

    # Checks for Mastercard id
    mastercard = True if cc_number_length == 16 and (cc_number_str[:2] == "51" or cc_number_str[:2] == "52" or
                                                     cc_number_str[:2] == "53" or cc_number_str[:2] == "54" or
                                                     cc_number_str[:2] == "55") else False

    # Checks for VISA id
    visa = True if (cc_number_length == 13 or cc_number_length == 16) and cc_number_str[:1] == "4" else False

    # Evaluates card id
    if amex:
        print("AMEX")
    elif mastercard:
        print("MASTERCARD")
    elif visa:
        print("VISA")
    else:
        print("INVALID")

else:
    print("INVALID")