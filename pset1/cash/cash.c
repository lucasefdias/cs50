// ------------------------------------------ //
// CS50 Problem Set 1: Cash
//
// Summary: Asks the user for an input (amount
// of change owed) and prints the number of
// coins necessary for the change
//
// Lucas Emidio Fernandes Dias
// 10 March 2018
// ------------------------------------------ //

// Include libraries
#include <stdio.h>
#include <cs50.h>
#include <math.h>

// Constants
#define QUARTER 25 // Quarter value
#define DIME 10    // Dime value
#define NICKEL 5   // Nickel value
#define PENNY 1    // Penny value

// ------------------------------------------ //
//        MAIN                                //
// ------------------------------------------ //
int main(void)
{
    float change; // Change owed (user input)

    // Asks the user for change value
    do
    {
        change = get_float("Change owed: ");
    }
    // Change is only valid if >= 0 and != string
    while (change < 0);

    // Convert to cents and round to int
    change *= 100;
    change = round(change);

    // Coins needed for change
    int coins = 0;

    // Quarter loop
    while (change >= QUARTER)
    {
        change -= QUARTER;
        coins++;
    }

    // Dime loop
    while (change >= DIME)
    {
        change -= DIME;
        coins++;
    }

    // Nickel loop
    while (change >= NICKEL)
    {
        change -= NICKEL;
        coins++;
    }

    // Penny loop
    while (change >= PENNY)
    {
        change -= PENNY;
        coins++;
    }

    // Print results
    printf("%i\n", coins);
}