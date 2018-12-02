// ------------------------------------------ //
// CS50 Problem Set 2: Crack
//
// Summary: Cracks a hashed password provided
// by the user
//
// Lucas Emidio Fernandes Dias
// 16 March 2018
// ------------------------------------------ //

// Crypt function requirements
#define _XOPEN_SOURCE
#include <unistd.h>

// Include libraries
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

// Constants
#define FALSE 0
#define TRUE !FALSE
#define HASH_MAX 14 // Hash max size for initializing arrays
#define PWD_MAX 5   // Passwords maximum size
#define SALT_MAX 3  // Salt array size (2 chars + NULL character)

// Function prototypes
int iterate_passwords(int pwd_size, int current_index, char key[], char hash[], char salt[]);

char shift_case(char letter);

// ------------------------------------------ //
//        MAIN                                //
// ------------------------------------------ //
int main(int argc, string argv [])
{
    // Error: missing hash argument
    if (argc < 2)
    {
        printf("Error: Missing an argument\n");
        printf("Usage: ./crack hash\n");
        return 1;
    }
    // Error: too many arguments
    else if (argc > 2)
    {
        printf("Error: Too many arguments\n");
        printf("Usage: ./crack hash\n");
        return 1;
    }
    // argc = 2: Run normal procedures
    else
    {
        // Initialize hash and salt array
        char hash[HASH_MAX];
        char salt[SALT_MAX];

        // Get hash and salt from argv[1]
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            // Get k from argv[1]
            hash[i] = argv[1][i];

            // Get salt (first 2 digits of hash)
            if (i < 2)
            {
                salt[i] = hash[i];
            }
        }

        // Iterate over key until password is cracked (all combinations from 1 to 5 char passwords)

        // Initialize key array (6 elements max: 5 letters + NULL character)
        char key[PWD_MAX + 1];

        // Iteration loop password size from 1 to 5 letters
        for (int pwd_size = 0; pwd_size < PWD_MAX; pwd_size++)
        {
            // Restart current_index to first letter of password
            int current_index = 0;

            // Call iteration function
            int pwd_found = iterate_passwords(pwd_size, current_index, key, hash, salt);

            // If password was found, break loop
            if (pwd_found)
            {
                return 0;
            }
        }

        // If password is longer than 5 characters, return error
        printf("Error: password could not be cracked\n");
        return 1;
    }
}

// Function declarations
// Iterate all passwords depending on password size
int iterate_passwords(int pwd_size, int current_index, char key[], char hash[], char salt[])
{
    for (key[current_index] = 'A'; key[current_index] <= 'z'; key[current_index]++)
    {
        // When uppercase characters finishes, move on to lowercase
        key[current_index] = shift_case(key[current_index]);

        // BASE CASE: current index is the pwd_size
        if (current_index == pwd_size)
        {
            // Add NULL character at the end of string
            key[pwd_size + 1] = '\0';

            // Check if password was found
            if (strcmp(crypt(key, salt), hash) == 0)
            {
                // Print password that was found
                for (int i = 0, m = strlen(key); i < m; i++)
                {
                    printf("%c", key[i]);
                }
                printf("\n");
                return TRUE;
            }
        }

        // RECURSIVE CASE: keep going through loops
        else if (current_index < pwd_size && key[pwd_size - 1] <= 'z')
        {

        }
        else
        {
            // Loop through next letter possibilities
            return iterate_passwords(pwd_size, current_index + 1, key, hash, salt);
        }
    }

    // Password not found
    return FALSE;
}

char shift_case(char letter)
{
    // When uppercase characters finishes, move on to lowercase
    if (!isalpha(letter))
    {
        return letter = 'a';
    }
    // Else, keep same character
    else
    {
        return letter;
    }
}