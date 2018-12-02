// ------------------------------------------ //
// CS50 Problem Set 2: Caesar
//
// Summary: Encrypts input messages using
// Caesar's cipher with a key input (k) from
// user
//
// Lucas Emidio Fernandes Dias
// 14 March 2018
// ------------------------------------------ //


// Include libraries
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

// Constants
#define ALPHABET_LETTERS 26
#define UPPER 1
#define LOWER 0

// Function prototypes
char encipher(char p, int k);

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
        printf("Usage: ./caesar k\n");
        return 1;
    }
    // Error: too many arguments
    else if (argc > 2)
    {
        printf("Error: Too many arguments\n");
        printf("Usage: ./caesar k\n");
        return 1;
    }
    // argc = 2: Run normal procedures
    else
    {
        // Get k from argv and convert string to int
        int k = atoi(argv[1]);

        // Get plaintext
        printf("plaintext:  ");
        string p = get_string();

        // Encipher and then print ciphertext
        printf("ciphertext: ");

        for (int i = 0, n = strlen(p); i < n; i++)
        {
            // If alphabetic character, shift by key (encipher)
            if (isalpha(p[i]))
            {
                p[i] = encipher(p[i], k);
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
char encipher(char p, int k)
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