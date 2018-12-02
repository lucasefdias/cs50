// ------------------------------------------ //
// CS50 Problem Set 1: Mario (less)
//
// Summary: Prints Mario`s pyramid (less)
//
// Lucas Emidio Fernandes Dias
// 9 March 2018
// ------------------------------------------ //


// Include libraries
#include <stdio.h>
#include <cs50.h>

// ------------------------------------------ //
//        MAIN                                //
// ------------------------------------------ //
int main(void)
{
    int height; // Height of the pyramid (user input)

    // Asks the user for a height
    do
    {
        height = get_int("Height: ");
    }
    // Height is only valid if 0 <= height <= 23
    while (height < 0 || height > 23);

    // Prints the pyramid
    for (int i = 0; i < height; i++)
    {
        // Print spaces
        for (int j = 0; j < height - i - 1; j++)
        {
            printf(" ");
        }
        // Print hashes
        for (int j = 0; j < i + 2; j++)
        {
            printf("#");
        }
        // Print new line
        printf("\n");
    }
}