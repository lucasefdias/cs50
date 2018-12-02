// ------------------------------------------ //
// CS50 Problem Set 2: Vigenère
//
// Summary: Encrypts input messages using
// Vigenère's cipher with a key input (k) from
// user
//
// Lucas Emidio Fernandes Dias
// 15 March 2018
// ------------------------------------------ //


// Include libraries
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

// Constants
#define ALPHABET_LETTERS 26
#define UPPER 1 // Indicates uppercase
#define LOWER 0 // Indicates lowercase
#define MAX 100 // Maximum keyword size

// Function prototypes
char encipher(char p, char k);

char ascii_to_alpha(char p, int key);

char alpha_to_ascii(char p, int key);

// ------------------------------------------ //
//        MAIN                                //
// ------------------------------------------ //
int main(int argc, string argv [])
{
    // Error: missing k argument
    if (argc < 2)
    {
        printf("Error: Missing an argument\n");
        printf("Usage: ./vigenere k\n");
        return 1;
    }
    // Error: too many arguments
    else if (argc > 2)
    {
        printf("Error: Too many arguments\n");
        printf("Usage: ./vigenere k\n");
        return 1;
    }
    // argc = 2: Run normal procedures
    else
    {
        // Initialize keyword array
        char k[MAX];

        // Check if argv[1] contains only alpabetical characters
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            // Exit program if argv[1] contains non-alphabetical characters
            if (!isalpha(argv[1][i]))
            {
                printf("Error: Argument must contain only alphabetical characters\n");
                printf("Usage: ./vigenere k\n");
                return 1;
            }

            // Get k from argv[1]
            k[i] = argv[1][i];

            // Convert from ASCII to alphabetical index
            // Uppercase
            if (isupper(k[i]))
            {
                k[i] = ascii_to_alpha(k[i], UPPER);
            }
            // Lowercase
            else
            {
                k[i] = ascii_to_alpha(k[i], LOWER);
            }
        }

        // Get plaintext
        printf("plaintext:  ");
        string p = get_string();

        // Encipher and then print ciphertext
        printf("ciphertext: ");

        // Loop through plaintext (p)
        // i: p counter; j: k counter
        for (int i = 0, j = 0, n = strlen(p), m = strlen(argv[1]); i < n; i++)
        {
            // If alphabetic character, shift by key (encipher)
            if (isalpha(p[i]))
            {
                // Encipher p[i] using k[j]
                p[i] = encipher(p[i], k[j]);
                // Moves to next k element
                j = (j + 1) % m;
            }

            // Print ciphertext character
            printf("%c", p[i]);
        }

        printf("\n");

        return 0;
    }
}

// Function declarations

// Enciphers alphabetical characters
char encipher(char p, char k)
{
    int key;

    // Check char case (uppercase or lowercase)
    if (isupper(p))
    {
        key = UPPER;
    }
    else
    {
        key = LOWER;
    }

    // Convert ASCII index to alphabetical index
    p = ascii_to_alpha(p, key);

    // Shift plaintext character by key
    p = (p + k) % ALPHABET_LETTERS;

    // Convert ASCII index to alphabetical index
    p = alpha_to_ascii(p, key);

    return p;
}

// Converts ASCII index to alphabetical index
char ascii_to_alpha(char p, int key)
{
    // For uppercase
    if (key == UPPER)
    {
        return p -= 'A';
    }
    // For lowercase
    else
    {
        return p -= 'a';
    }
}

// Converts ASCII index to alphabetical index
char alpha_to_ascii(char p, int key)
{
    // For uppercase
    if (key == UPPER)
    {
        return p += 'A';
    }
    // For lowercase
    else
    {
        return p += 'a';
    }
}