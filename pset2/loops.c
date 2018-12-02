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
#define TRUE 1
#define FALSE 0
#define HASH_MAX 14 // Hash max size for initializing arrays
#define PWD_MAX 6   // Passwords array size (5 chars plus NULL char)
#define SALT_MAX 3  // Salt array size

// Function prototypes
int iterate_char(int pwd_size, char key[], char hash[], char salt[]);

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

        // Initialize key array
        char key[PWD_MAX];

        // 1 char
        // Defines key array highest index
        int pwd_size = 0;

        if (iterate_char(pwd_size, key, hash, salt) == TRUE)
        {
            return 0;
        }

        // 2 chars
        // Defines key array highest index
        pwd_size = 1;

        for (key[0] = 'A'; key[0] <= 'z'; key[0]++)
        {
            key[0] = shift_case(key[0]);

            if (iterate_char(pwd_size, key, hash, salt) == TRUE)
            {
                return 0;
            }
        }

        // 3 chars
        // Defines key array highest index
        pwd_size = 2;

        for (key[0] = 'A'; key[0] <= 'z'; key[0]++)
        {
            key[0] = shift_case(key[0]);

            for (key[1] = 'A'; key[1] <= 'z'; key[1]++)
            {
                key[1] = shift_case(key[1]);

                if (iterate_char(pwd_size, key, hash, salt) == TRUE)
                {
                    return 0;
                }
            }
        }

        // 4 chars
        // Defines key array highest index
        pwd_size = 3;

        for (key[0] = 'A'; key[0] <= 'z'; key[0]++)
        {
            key[0] = shift_case(key[0]);

            for (key[1] = 'A'; key[1] <= 'z'; key[1]++)
            {
                key[1] = shift_case(key[1]);

                for (key[2] = 'A'; key[2] <= 'z'; key[2]++)
                {
                    key[2] = shift_case(key[2]);

                    if (iterate_char(pwd_size, key, hash, salt) == TRUE)
                    {
                        return 0;
                    }
                }
            }
        }

        // 5 chars
        // Defines key array highest index
        pwd_size = 4;

        for (key[0] = 'A'; key[0] <= 'z'; key[0]++)
        {
            key[0] = shift_case(key[0]);

            for (key[1] = 'A'; key[1] <= 'z'; key[1]++)
            {
                key[1] = shift_case(key[1]);

                for (key[2] = 'A'; key[2] <= 'z'; key[2]++)
                {
                    key[2] = shift_case(key[2]);

                    for (key[3] = 'A'; key[3] <= 'z'; key[3]++)
                    {
                        key[3] = shift_case(key[3]);

                        if (iterate_char(pwd_size, key, hash, salt) == TRUE)
                        {
                            return 0;
                        }
                    }
                }
            }
        }

        // If password is longer than 5 characters, return error
        printf("Error: password could not be cracked\n");
        return 1;
    }
}

// Function declarations

// Checks all possibilites of alphabetical characters for one char
int iterate_char(int pwd_size, char key[], char hash[], char salt[])
{
    for (key[pwd_size] = 'A'; key[pwd_size] <= 'z'; key[pwd_size]++)
    {
        // When uppercase characters finishes, move on to lowercase
        key[pwd_size] = shift_case(key[pwd_size]);

        // Check if password was found
        if (strcmp(crypt(key, salt), hash) == 0)
        {
            // Print password found
            for (int i = 0, m = strlen(key); i < m; i++)
            {
                printf("%c", key[i]);
            }
            printf("\n");
            return TRUE;
        }
    }
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