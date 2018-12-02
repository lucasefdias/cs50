# ----------------------------------------------
# CS50 Problem Set 6: Sentimental - Cash
#
# Summary: Reimplements Cash in Python
# Asks the user for an input (amount of change
# owed) and prints the number of coins necessary
# for the change
#
# Lucas Emidio Fernandes Dias
# 03 October 2018
# ----------------------------------------------

from cs50 import get_float

# Constants
QUARTER = 25
DIME = 10
NICKEL = 5
PENNY = 1

# Prompts the user for change value until it is a valid unput

while True:

    change = get_float("Change owed: ")

    if change > 0:
        break

# Convert to cents and round to int
change *= 100
change = round(change)

# Coins needed for change
coins = 0

# Quarter loop
while change >= QUARTER:
    change -= QUARTER
    coins += 1

# Dime loop
while change >= DIME:
    change -= DIME
    coins += 1

# Nickel loop
while change >= NICKEL:
    change -= NICKEL
    coins += 1

# Penny loop
while change >= PENNY:
    change -= PENNY
    coins += 1

# Print results
print(coins)