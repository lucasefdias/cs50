// ------------------------------------------ //
// CS50 Problem Set 1: Credit
//
// Summary: Asks the user for an input (number)
// and evaluates if the input is a valid credit
// card number
//
// Lucas Emidio Fernandes Dias
// 12 March 2018
// ------------------------------------------ //


// Include libraries
#include <stdio.h>
#include <cs50.h>

// ------------------------------------------ //
//        MAIN                                //
// ------------------------------------------ //
int main(void)
{
    long long cc_number; // Credit card number (user input)

    // Asks the user for a number
    do
    {
        cc_number = get_long_long("Number: ");
    }
    // Number is only valid if >= 0 and != string
    while (cc_number < 0);

    // Number length
    int length = 0;

    // Checksum
    int checksum = 0;

    // Company identifier
    int id;

    // Checksum procedure
    while (cc_number > 0)
    {

        // Increase length
        length ++;

        // Every other digit procedure
        if (length % 2 == 0)
        {
            int every_other = cc_number % 10;

            every_other *= 2;

            if (every_other >= 10)
            {
                checksum += (every_other % 10) + (every_other / 10);
            }
            else
            {
                checksum += every_other;
            }
        }
        // Remaining digits procedure
        else
        {
            int digit = cc_number % 10;

            checksum += digit;
        }

        // Gets first digits identifier
        if (cc_number < 100 && cc_number >= 10)
        {
            id = 10 * (cc_number / 10) + (cc_number % 10);
        }
        // If id is not AMEX or MASTERCARD, get first digit
        else if (cc_number < 10 && (id != 34 && id != 37 && id != 51
                                    && id != 52 && id != 53 && id != 54 && id != 55))
        {
            id = cc_number;
        }

        // Truncates last digit
        cc_number /= 10;
    }

    // If sum is valid, evaluates identifier. Else, card number is invalid.
    if ((checksum % 10) == 0)
    {
        // American Express
        if (length == 15 && (id == 34 || id == 37))
        {
            printf("AMEX\n");
        }
        // MasterCard
        else if (length == 16 && (id == 51 || id == 52 ||
                                  id == 53 || id == 54 || id == 55))
        {
            printf("MASTERCARD\n");
        }
        // Visa
        else if ((length == 13 || length == 16) && id == 4)
        {
            printf("VISA\n");
        }
        // Invalid number
        else
        {
            printf("INVALID\n");
        }
    }
    // Invalid number
    else
    {
        printf("INVALID\n");
    }
}